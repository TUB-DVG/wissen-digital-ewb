from django.core.serializers.json import Serializer as DefaultSerializer

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
                    pk if pk.remote_field and pk.remote_field.parent_link else None
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
                if (
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
        """handle the backward referenced field

        """
        # breakpoint()
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

        m2m_iter = getattr(obj, "_prefetched_objects_cache", {}).get(
            field.name,
            queryset_iterator(obj, field),
        )
        self._current[field.name] = [m2m_value(related) for related in m2m_iter]
