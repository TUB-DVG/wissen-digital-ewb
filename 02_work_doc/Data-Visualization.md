# Data visualization for web development:
As we now reached the point in our project where we would like to start adding graphical features. I did a thorough research about the different data visualization options that we could to integrate into our Django project, so we can have an informed discussion on how to proceed and what tools should we use going forward.

There multiple languages that are used for data visualization, However 2 standout in particular: python and JavaScript.
## Python: 

    • Functionality: JavaScript just doesn’t have the range of data science packages and inbuilt functionality compared to languages such as Python. If you don’t mind reinventing the wheel, this might be less of an issue.
    • Productivity: Another advantage of Python extensive ecosystems is there are many guides and how-to’s available for almost any data science task you wish to do. For JavaScript, this is not really the case. You will probably take longer figuring out how to solve a data science problem in JavaScript than you would in Python .
    • Simplicity: Python is much simpler than JavaScript (one of the simplest programming languages)
    • Time: Learning JavaScript will take quite a bit of time that can be used developing functionalities in python.
    • Data Manipulation: Python has one of the best string manipulation library of all time. It’s seamless and hassle free to work with. JavaScript on the other hand is SIGNIFICANTLY tougher to work with on this.
    • Machine Learning: Python is much more equipped for machine learning tasks, which will use later on.

## JavaScript:

    • Visualization: JavaScript excels at data visualization. Libraries such as D3.js, Chart.js, Plotly.js and many others make powerful data visualization and dashboards easy to build and provide a variety of options and flexibility that python does not have.
    • Speed: For Web Applications, JS will be faster because it is baked into the browsers, all browsers have a built-in JS engine.
    • Displaying on web fronts is much easier through JavaScript ( JS works well with HTML and CSS).

Sources: Discussion with 4 desginers/developpers(In English)

https://www.youtube.com/watch?v=Awnz8x8kcE8



## Python Libraries:

In this Section, I have compiled a list of links to the galleries and descriptions of the best python data_visualisation libraries.

7 Must-Try Data Visualization Libraries in Python:

https://betterprogramming.pub/7-must-try-data-visualization-libraries-in-python-fd0fe76e08a0

* Bokeh:

https://docs.bokeh.org/en/latest/docs/gallery.html

https://docs.bokeh.org/en/latest/docs/first_steps.html#first-steps

Integration with Django:
https://hackernoon.com/integrating-bokeh-visualisations-into-django-projects-a1c01a16b67a

* ggplot: 
https://yhat.github.io/ggpy/

* Seaborn: 

https://seaborn.pydata.org/examples/index.html

* Plotly:

https://plotly.com/python/

Integration with Django:
https://www.codingwithricky.com/2019/08/28/easy-django-plotly/


-From the above mentionned python Libraries, in my opinion, 2 stand out in particular: Bokeh and Plotly. Both libraries seem to be more developed than the rest and have more features for interactivity(widgets) and there seems to be quite more documentation about Django integration of those 2 libraries.

### Plotly vs Bokeh:
https://pauliacomi.com/2020/06/07/plotly-v-bokeh.html

* 3D graphs: Bokeh has no inherent 3D graphing functionality however Plotly has that.
* Data handling: While both libraries can easily take lists, arrays and DataFrames as data, a key feature of Bokeh comes in the form of a ColumnDataSource, a custom data storage class which can be considered somewhere between a pandas.DataFrame and a dict. It can be passed to multiple graphs, which results in a shared dataset, linked between all visualisations. What is more, data contained within can be easily appended or patched, making dashboards which rely on very large datasets much quicker to update.






## JavaScript Libraries:
In this Section, I have compiled a list of links to the galleries and descriptions of the best JavaScript data_visualisation libraries.

* D3.js:

https://www.d3-graph-gallery.com/

https://www.d3-graph-gallery.com/graph/circularpacking_template.html

* Chart.js:

https://www.chartjs.org/

* Plotly.js (same as the python library):

https://plotly.com/javascript/


-This link provides a very good comparison of the 3 libraries:

https://www.slant.co/topics/3335/versus/~d3-js_vs_chart-js_vs_plotly

