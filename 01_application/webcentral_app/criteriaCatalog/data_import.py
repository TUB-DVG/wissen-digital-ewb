from .models import (
    CriteriaCatalog,
    Topic,
    Tag,
)
from common.data_import import DataImport

class DataImportApp(DataImport):
    def __init__(self, path_to_data_file):
        """Constructor of the app-specific data_import

        Calls the constructor of the parent class `DataImport`.
        The parent-class then handles the read in process of the
        file, whose file-path was given as `path_to_data_file`.

        path_to_data_file:  str
            Represents the file-path to the Data-File (xlsx or csv).
        """
        super().__init__(path_to_data_file)
    
    def getOrCreate(self, row: list, header: list, data: list) -> None:
        """
        Add entry (CriteriaCatalog) into the table or/and return entry key.
        """

        criteriaCatalogForTopic, _ = CriteriaCatalog.objects.get_or_create(
            name=row[header.index("katalog")], )


        try:
            if row[header.index("parentId")] == "":
                parentTopicOfCurrentTopic = None
            else:
                for rowToBeSearchedForParent in data:
                    if rowToBeSearchedForParent[header.index("id")] == row[header.index("parentId")]:
                        parentIdRow = rowToBeSearchedForParent
                        break
                if parentIdRow is not None:
                    # find also the parent of the parent since Topics can be identical
                    if parentIdRow[header.index("parentId")] != "":
                        for rowToBeSearchedForParent in data:
                            if rowToBeSearchedForParent[header.index("id")] == parentIdRow[header.index("parentId")]:
                                parentOfParentRow = rowToBeSearchedForParent
                                break
                        parentOfParent = Topic.objects.get(
                            heading=parentOfParentRow[header.index("ueberschrift")],
                            text=parentOfParentRow[header.index("text")],
                            criteriaCatalog=criteriaCatalogForTopic,
                            topicHeadingNumber=parentOfParentRow[header.index("id2")],
                        )

                    else:
                        parentOfParent = None
                    parentTopicOfCurrentTopic = Topic.objects.filter(
                        heading=parentIdRow[header.index("ueberschrift")],
                        text=parentIdRow[header.index("text")],
                        criteriaCatalog=criteriaCatalogForTopic,
                        parent=parentOfParent,
                        topicHeadingNumber=parentIdRow[header.index("id2")],
                    )
                     
                    if len(parentTopicOfCurrentTopic) > 1:
                        breakpoint()
                    parentTopicOfCurrentTopic = parentTopicOfCurrentTopic[0]
        except Topic.DoesNotExist:
            parentTopicOfCurrentTopic = None
        obj, created = Topic.objects.get_or_create(
            heading=row[header.index("ueberschrift")],
            text=row[header.index("text")],
            criteriaCatalog=criteriaCatalogForTopic,
            parent=parentTopicOfCurrentTopic,
            imageFilename=row[header.index("image")],
            topicHeadingNumber=row[header.index("id2")],
        )

        if row[header.index("tags")] != "" or row[header.index("tags")] == " ":
            tagList = row[header.index("tags")].split(",")
            for tag in tagList:
                tagObj, _ = Tag.objects.get_or_create(name=tag)
                obj.tag.add(tagObj)
            obj.save()

