## Adding Image Field to model:
Some Models (Database Objects) may require images, this can be achieved 
through the FileField called "ImageField" in Django .To use this field 
properly, you need to install the package "pillow" to your python environment.

```
image=models.ImageField(default="Default.webp",blank = True) 
# The default variable sets the default image for the model entry 
in case no image has been provided. 
```
The ImgaeField has an attribute url that can be used to be used to display the image in html

```
<img src=" {{ model_object.image.url }}" >
```
In order for Django to know where to store and to find images to display
them, the url must be set up in settings and urls python files 
(both files should be in the Directory of THE PROJECT not the apps).

```
At the bottom of the settings.py file add this line :

MEDIA_ROOT=Path.joinpath(BASE_DIR,'Where you want the images that are uploaded to be stored')
# This will set the Media_ROOT as the default folder where the images will be stored.

At the bottom of the urls.py file add this line :
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# This will link the url attribute that the image field has to the media_root 
that you set up in settings.py
```

## Adding Search/Filter functionalities:
The idea of the search and filter functionalities is the same, if we 
can get some information from the user of our webpage through an html 
button or query then based on that information we can filter the searched 
object and return the filtered object back to the html for rendering.


#### Acquiring data from html and sending it to the View function for filtering:

We can get data from an html using different tags depending on the use case: 
For search purposes, we use the input tag since it allows us to provide
a field where the user can input a search keyword.
For filtering, the select tag is mainly used since it provides the user 
with multiple options for selection. The tags that have information 
that is intended to be used by view function or further display are required 
to have the "name" attribute( see example below).

To send data we use the form tag, the method attribute of this tag 
specifies how to send form-data (the form-data is sent to the page specified in the action attribute). 
The form-data can be sent as URL variables (with method="get" ) 
or as HTTP post transaction (with method="post" ). 

GET is used for viewing something, without changing it, while POST is used for changing something.
For example, a search page should use GET to get data while a form that 
changes your password should use POST.
Essentially GET is used to retrieve remote data, and POST is used to insert/update remote data.

Example:
```
 <form action="/action_page.html" method="get">
  <label for="fname">First name:</label>
  <input type="text" id="fname" name="fname"><br><br>
  <label for="lname">Last name:</label>
  <input type="text" id="lname" name="lname"><br><br>
  <input type="submit" value="Submit">
</form>     

#In this example we are sending to the action_page.html file information that was typed in 
the 2 input tags named "fname" and "lname" through url variables (Method='get').

```
Instead of using the action attribute, the href attribute can be used as
well in the input/button tags with attribute ' type="submit" ' to send data
to a url instead of page which is what we will use for our functionality since we would like to send the data to a view function.

```
<input type="submit" value="Submit" href="{% url'Views_function_name'%}">

```
Now that the data has been sent, We will look at how to acces it through our views function.

In Django every Views.function has a parameter named request. 
That parameter contains the url information that was sent to the url 
associated with that view.function.Meaning once we receive a request to the 
url associated with that function : Do whatever is defined in the function 
with the information contained in the request.

In this case, we have the search/filter information inside that request, 
to acces that data we use the command:
```
if (request.GET.get("lname") != None):
        left_name=request.GET.get('lname')

# If the request information that was sent through the "GET" method under
the name "lname" is available ( !=None), then save that information into left_name.
Now the left_name variable holds the information that was sent through
 the input named "lname" of our previous form.
```

If we would like to process a request with multiple information at once,
we can update the command as follows:
```
if ((request.GET.get("lname") != None) | (request.GET.get("rname") != None)) :
        left_name=request.GET.get('lname')
        right_name=request.GET.get('rname')

# With this command we will access the request data if one or both information is available.
# If the information of one of them is not available(input is empty) 
then the corresponding variable will hold None.
```
#### Sending objects from View function to html files:

Through Django View functions, one can send an html template model.object data to be rendered:

```
    context = {
        'variable1': page,

        }

    return render(request, 'tools_over/tool-listings.html', context)

# This return command at the end of the view function renders the given html
( the one between '') while providving it with the contents of the variable context.
# In the example above we are rendering the tool-listings html file 
while providing it with the variable page, the name between '' is the 
name that is used to acces the page variable in the html.
```


## Adding pagination to Django display:
When displaying Django model objects, You want to limit 
the number of obejcts displayed per page.
This can be done through Pagination in the Django Views functions

```
tools_paginator= Paginator (objects,12) # divide the objects into pages with each holding 12 objecst
page_num= request.GET.get('page',None) # Get the current page number
variable=tools_paginator.get_page(page_num) # save the objects on that page to variable

```

## Example Implementation:
Example Implementation of the previously discussed features:

```
# Class Tools in models.py:

class Tools(models.Model):
    bezeichnung = models.CharField(max_length = 150,
                                   help_text="Name der Anwendung",
                                   blank = True)
    kategorie = models.CharField(max_length = 100,
                                 help_text = "Kategorie in der die Anwendung eingeordnet werden kann",blank = True)
---------------------------------------------------------------------------------------------
#View function for search display and filter by Kategorie display
def index(request):
    """
    shows the list of all Tools filtered according to some key features
    """
    tools = Tools.objects.all() # reads all data from model Tools

    filtered_by = [None]*3 # Setting up the filter options
    searched=None # Setting the searched keyword 


 
    if ((request.GET.get("1") != None)|(request.GET.get("searched") != None)):
        Kategorie=request.GET.get('1')
        searched=request.GET.get('searched')
        tools=Tools.objects.filter(kategorie__icontains=Kategorie,bezeichnung__icontains=searched) #filter the model Tools based on if the attribute Kategorie of the model contains the filtered kategorie and the bezeichnung of the model attribute contains the searched keyword.
        filtered_by = [Kategorie]
              

    tools_paginator= Paginator (tools,12) #Display only 12 tools per page
    page_num= request.GET.get('page',None) # receive the current page number from the request 
    page=tools_paginator.get_page(page_num) # save all the tools on that page to the variable pgae

       
    context = {
        'page': page,
        'search':searched,
        'kategorie': filtered_by[0],
        
    }

    return render(request, 'tools_over/tool-listings.html', context)


------------------------------------------------------------------------
#Html that sends the kategorie filter and the searched keyword to the viewfunction:


<form  method="GET">
    <div class="col-xl-3" >
        <input  type="search" placeholder="Suchbegriff" name='searched'>
    </div>
    <div class="row g-3">
        <!-- Select items -->
    <div c>
            <select name="1"> 
                
                <option value="">Kategorien</option>
                
                <option value="Datenverwaltung">Datenverwaltung</option>
                <option value="Anzeige und Gestaltung">Anzeige und Gestaltung</option>
                <option value="Modellbildung">Modellbildung</option>
                <option value="Cloud-basiertes Echtzeit Monitoring">Cloud-basiertes Echtzeit Monitoring</option>
                <option value="Programmiersprache" >Programmiersprache</option>
                <option value="Konstruktion">Konstruktion</option>
                <option value="Cloud Anwendung">Cloud Anwendung</option>
                <option value="Analyse">Analyse</option>
                <option value="Modellierung">Modellierung</option>
                <option value="Simulation">Simulation</option>
                <option value="Energiemanagement">Energiemanagement</option>
                <option value="Betriebsoptimierung">Betriebsoptimierung</option>
                <option value="Datenbankmanagement">Datenbankmanagement</option>
                <option value="Berechnung">Berechnung</option>
                <option value="Programmierumgebung">Programmierumgebung</option>
                <option value="Visualisierung">Visualisierung</option>
                <option value="Modellanalyse">Modellanalyse</option>
                <option value="Machine Learning">Machine Learning</option>

            </select>
            
        </div>
        <div >
            <button type="submit" href=""><i class="fas fa-search"></i></button>
        </div>
</form>

# The href attribute is here empty since we would like to acces the same url
```

## Rating Feature:

To add a Rating Feature:
First, we need to create a model that will link the user that does
the rating and the rated object.
Example:
```
#Rating that contains a score from 0 to 5 and a comment for our Tool Model mentioned above:
class Rating (models.Model):
    rating_from = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='rating_from')
    rating_for = models.ForeignKey("Tools", on_delete=models.SET_NULL, null=True, related_name='rating_for')
    comment=models.CharField(max_length=1000,blank=True)
    score=models.IntegerField  ( default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
     )

```
Using the features mentioned above( Sending data between html and view functions),
we can receive the rating data provided by the user for the corresponding 
Tool and then in a view function save that data as a Rating model entry.
Unlike with the search functionality, we are now trying to save the received
data i.e changing the Rating model,so we will the used the method 'POST'.
( With the 'post' method a {% csrf_token %} must be used before every tag that holds information to be sent.)

Example Implementation:
```    
#html:
<div>
    <h5 c>Leave a Rating</h5>
    <form  action="/tool_list/Post_Rating/{{tool.id}} method="post">
        {% csrf_token %}
        <!-- Score -->
        <div >
            <select name='score' >
                <option selected=""value="5">★★★★★ (5/5)</option>
                <option value="4">★★★★☆ (4/5)</option>
                <option value="3">★★★☆☆ (3/5)</option>
                <option value="2">★★☆☆☆ (2/5)</option>
                <option value="1">★☆☆☆☆ (1/5)</option>
            </select>
        </div>

        <!-- Comment -->
        {% csrf_token %}
        <div >
            <textareaplaceholder="Your Comment"  name='comment'></textarea>
        </div>

        <button type="submit" href="" >Post Review</button>   
    </form>
</div>
```  

View function:
The id of the rated object needed to be received either as part of the 
request data or as its own parameter, in this case we opted to receive 
it as it's own variable and for that the urls python file must be updated
by adding this url pattern:
```  
path('Post_Rating/<str:id>', views.Post_Rating, name='Post_Rating'),
# the <str:id> holds the id that the view function will get as a parameter.
```  
Example implmentation of the view function Post_Rating:
```  
def Post_Rating(request,id):
    if request.method=="POST":
        User=request.user # The user that rated in the one that sent the request
        tool= get_object_or_404(Tools, pk= id)
        comment=request.POST['comment'] # Sent from the html (above)
        score=request.POST['score'] # Sent from the html (above)

        rating=Rating.objects.create(rating_from=User,rating_for=tool,score=score,comment=comment) # Create a model object with the new data.

        return  something # A place holder for what should the function return after execution
```
## Tool Tips:

A mouse-over description is possible through the title attribute that 
works with all HTML tags(It's a global attribute).

```
<div title="description">

# When we mouse over the division or section defined above,
the "description will appead under the mouse cursor"
```