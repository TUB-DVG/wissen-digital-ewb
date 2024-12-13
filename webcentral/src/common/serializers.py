import json

from django.apps import apps
from django.core.serializers.json import Serializer as DefaultSerializer
from django.db import DEFAULT_DB_ALIAS, models
from django.core.serializers import base
from django.core.serializers.base import DeserializationError


class Serializer(DefaultSerializer):
    """This class extends the json-serializer from the django core. It is needed
    since the default Json serializer does not include the backward reference of
    a Many-to-Many relation. By a backward reference, a reference is meant, which
    does not appear in the to be serialized django model. Instead the django model
    appears in another model as for e.g. a `ManyToManyField`.

    """

    def serialize(
        self,
        queryset,
        *,
        stream=None,
        fields=None,
        use_natural_foreign_keys=False,
        use_natural_primary_keys=False,
        progress_output=None,
        object_count=0,
        **options,
    ):
        """
        Override the serialize method from the serializer base class and add
        logic to handle backward references.
        """
        self.options = options

        self.stream = stream if stream is not None else self.stream_class()
        self.selected_fields = fields
        self.use_natural_foreign_keys = use_natural_foreign_keys
        self.use_natural_primary_keys = use_natural_primary_keys
        progress_bar = self.progress_class(progress_output, object_count)

        self.start_serialization()
        self.first = True
        for count, obj in enumerate(queryset, start=1):
            self.start_object(obj)
            # Use the concrete parent class' _meta instead of the object's _meta
            # This is to avoid local_fields problems for proxy models. Refs #17717.
            concrete_model = obj._meta.concrete_model
            # When using natural primary keys, retrieve the pk field of the
            # parent for multi-table inheritance child models. That field must
            # be serialized, otherwise deserialization isn't possible.
            if self.use_natural_primary_keys:
                pk = concrete_model._meta.pk
                pk_parent = (
                    pk
                    if pk.remote_field and pk.remote_field.parent_link
                    else None
                )
            else:
                pk_parent = None
            for field in concrete_model._meta.local_fields:
                if field.serialize or field is pk_parent:
                    if field.remote_field is None:
                        if (
                            self.selected_fields is None
                            or field.attname in self.selected_fields
                        ):
                            self.handle_field(obj, field)
                    else:
                        if (
                            self.selected_fields is None
                            or field.attname[:-3] in self.selected_fields
                        ):
                            self.handle_fk_field(obj, field)
            for field in concrete_model._meta.local_many_to_many:
                if field.serialize:
                    if (
                        self.selected_fields is None
                        or field.attname in self.selected_fields
                    ):
                        self.handle_m2m_field(obj, field)
            for field in concrete_model._meta.related_objects:
                if hasattr(obj, field.name + "_set") and (
                    self.selected_fields is None
                    or field.attname in self.selected_fields
                ):
                    self.handle_backward_m2m_field(obj, field)

            self.end_object(obj)
            progress_bar.update(count)
            self.first = self.first and False
        self.end_serialization()
        return self.getvalue()

    def handle_backward_m2m_field(self, obj, field):
        """handle the backward referenced field"""
        # if field.remote_field.through._meta.auto_created:
        if self.use_natural_foreign_keys and hasattr(
            field.remote_field.model, "natural_key"
        ):

            def m2m_value(value):
                return value.natural_key()

            def queryset_iterator(obj, field):
                return getattr(obj, field.name + "_set").iterator()

        else:

            def m2m_value(value):
                return self._value_from_field(value, value._meta.pk)

            def queryset_iterator(obj, field):
                return (
                    getattr(obj, field.name)
                    .select_related(None)
                    .only("pk")
                    .iterator()
                )

        if field.name == "customlink" or field.name == "customfile":
            return
        m2m_iter = getattr(obj, "_prefetched_objects_cache", {}).get(
            field.name,
            queryset_iterator(obj, field),
        )
        self._current[field.name] = [m2m_value(related) for related in m2m_iter]


def PythonDeserializer(
    object_list, *, using=DEFAULT_DB_ALIAS, ignorenonexistent=False, **options
):
    handle_forward_references = options.pop("handle_forward_references", False)
    field_names_cache = {}  # Model: <list of field_names>
    for d in object_list:
        # Look up the model and starting build a dict of data for it.
        try:
            Model = _get_model(d["model"])
        except base.DeserializationError:

            if ignorenonexistent:
                continue
            else:
                raise

        data = {}
        if "pk" in d:
            try:
                data[Model._meta.pk.attname] = Model._meta.pk.to_python(
                    d.get("pk")
                )
            except Exception as e:
                raise base.DeserializationError.WithData(
                    e, d["model"], d.get("pk"), None
                )
        m2m_data = {}
        deferred_fields = {}

        if Model not in field_names_cache:
            field_names_cache[Model] = {
                f.name for f in Model._meta.get_fields()
            }
        field_names = field_names_cache[Model]

        # Handle each field
        for field_name, field_value in d["fields"].items():
            if ignorenonexistent and field_name not in field_names:
                # skip fields no longer on model
                continue

            field = Model._meta.get_field(field_name)

            # Handle M2M relations
            if field.remote_field and isinstance(
                field.remote_field, models.ManyToManyRel
            ):
                try:
                    values = base.deserialize_m2m_values(
                        field, field_value, using, handle_forward_references
                    )
                except base.M2MDeserializationError as e:
                    raise base.DeserializationError.WithData(
                        e.original_exc, d["model"], d.get("pk"), e.pk
                    )
                if values == base.DEFER_FIELD:
                    deferred_fields[field] = field_value
                else:
                    m2m_data[field.name] = values
            # Handle FK fields
            elif field.remote_field and isinstance(
                field.remote_field, models.ManyToOneRel
            ):
                try:
                    value = base.deserialize_fk_value(
                        field, field_value, using, handle_forward_references
                    )
                except Exception as e:
                    raise base.DeserializationError.WithData(
                        e, d["model"], d.get("pk"), field_value
                    )
                if value == base.DEFER_FIELD:
                    deferred_fields[field] = field_value
                else:
                    data[field.attname] = value
            # Handle all other fields
            elif isinstance(field, models.ManyToManyRel):
                if field.name in data.keys():
                    breakpoint()
            else:
                try:
                    data[field.name] = field.to_python(field_value)
                except Exception as e:
                    raise base.DeserializationError.WithData(
                        e, d["model"], d.get("pk"), field_value
                    )

        obj = base.build_instance(Model, data, using)
        yield base.DeserializedObject(obj, m2m_data, deferred_fields)


def Deserializer(stream_or_string, **options):
    """
    Deserialize simple Python objects back into Django ORM instances.

    It's expected that you pass the Python objects themselves (instead of a
    stream or a string) to the constructor
    """
    if not isinstance(stream_or_string, (bytes, str)):
        stream_or_string = stream_or_string.read()
    if isinstance(stream_or_string, bytes):
        stream_or_string = stream_or_string.decode()
    try:
        objects = json.loads(stream_or_string)
        yield from PythonDeserializer(objects, **options)
    except (GeneratorExit, DeserializationError):
        raise
    except Exception as exc:
        raise DeserializationError() from exc


def _get_model(model_identifier):
    """Look up a model from an "app_label.model_name" string."""
    try:
        return apps.get_model(model_identifier)
    except (LookupError, TypeError):
        raise base.DeserializationError(
            "Invalid model identifier: '%s'" % model_identifier
        )
