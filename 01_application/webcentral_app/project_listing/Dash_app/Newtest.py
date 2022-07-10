from django_plotly_dash import DjangoDash
from dash import dcc, html
from dash.dependencies import Output, Input
import flask
import glob
import os

image_directory = r'C:\Users\Drass\plotly dash\webcentral\01_application\webcentral_app\webcentral_app\static\User_Images'
list_of_images= [file for file in os.listdir(image_directory) if file.endswith('solar.png')]
print(list_of_images)
static_image_route = '/static/User_Images/'

app = DjangoDash('NewTest')

app.layout = html.Div([
    dcc.Dropdown(
        id='image-dropdown',
        options=[{'label': i, 'value': i} for i in list_of_images],
        value=None
    ),
    html.Img(id='image')
])
@app.callback(
    Output('image', 'src'),
    [Input('image-dropdown', 'value')])
def update_image_src(value):
    return static_image_route + value

# Add a static image route that serves images from desktop
# Be *very* careful here - you don't want to serve arbitrary files
# from your computer or server
