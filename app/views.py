from flask import Flask,request,get_flashed_messages,redirect,render_template,url_for,g,send_file
from app import app
from forms import *
from flask.ext.admin import helpers


from models import *


@app.route('/')
@app.route('/index')
def homepage():
	return render_template('index.html', 
        title="Homepage",user=None)

def serve_pil_image(pil_img):
    import StringIO
    img_io = StringIO.StringIO()
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

def generate_world_img(world):
	import Image
	img = Image.new('RGBA',(world.width(),world.height()))
	pixels = img.load()
	for y in range(0,world.height()):
		for x in range(0,world.width()):
			if world.tiles[y][x]=='S':
				pixels[x,y] = (0,0,255,255)
			elif world.tiles[y][x]=='M':
				pixels[x,y] = (90,90,15,255)
			elif world.tiles[y][x]=='H':
				pixels[x,y] = (137,171,53,255) 
				#pixels[x,y] = (255,0,0,255) 
			elif world.tiles[y][x]=='D':
				pixels[x,y] = (241,247,67,255) 
			elif world.tiles[y][x]=='W':
				pixels[x,y] = (140,140,60,255) 						
			elif world.tiles[y][x]=='J':
				pixels[x,y] = (79,125,36,255)
			elif world.tiles[y][x]=='F':
				pixels[x,y] = (112,145,80,255)
			elif world.tiles[y][x]=='C':
				pixels[x,y] = (255,0,0,255)				
			else:
				pixels[x,y] = (0,255,0,255)
	return img

@app.route('/map/<worldname>.png')
def show_map_image(worldname):
    world = World.load(worldname)
    if world==None:
    	return "Request world does not exist"
    else:
    	img = generate_world_img(world)
    	return serve_pil_image(img)

@app.route('/world/<worldname>')
def show_world(worldname):
    world = World.load(worldname)
    if world==None:
    	return "Request world does not exist"
    else:
    	return render_template('showorld.html', title="Map",user=None, world=world, cities=sorted(world.cities, key=lambda city: city.name))

@app.route('/createmap',methods=['GET','POST'])
def create_world_view():
	form = CreateMapForm(request.form)
	if request.method == 'POST' and form.validate():
		world = create_map(form.data['width'],form.data['height'],form.data['name'])	
		world.save()
		return redirect('/world/%s' % world.name)
	user = None
	#user=login.current_user 
	return render_template('createmap.html', 
        title="Create map",user=None,
        form=form)