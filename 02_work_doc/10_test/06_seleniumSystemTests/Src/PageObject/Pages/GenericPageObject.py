

class GenericPageObject(object):

    def getAllElementsOfTagname(self, tagname: str) -> list:
        """Returns a list of all elements with the given tagname.

        """
        return self.driver.find_elements(
            By.TAG_NAME,
            tagname,
        )
        