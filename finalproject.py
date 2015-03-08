from flask import Flask, render_template, request, redirect,jsonify, url_for
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Animal, PetItem

engine = create_engine('sqlite:///animalpet.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/animal/<int:animal_id>/menu/JSON')
def animalMenuJSON(animal_id):
	animal = session.query(Animal).filter_by(id = animal_id).one()
	items = session.query(PetItem).filter_by(animal_id = animal_id).all()
	return jsonify(PetItems=[i.serialize for i in items])

@app.route('/animal/<int:animal_id>/menu/<int:pet_id>/JSON')
def petItemJSON(animal_id, pet_id):
	Pet_Item = session.query(PetItem).filter_by(id = pet_id).one()
	return jsonify(Pet_Item = Pet_Item.serialize)

@app.route('/animal/JSON')
def animalsJSON():
	animals = session.query(Animal).all()
	return jsonify(animals= [r.serialize for r in animals])

#Show all animals
@app.route('/')
@app.route('/animal/')
def showAnimals():
	animals = session.query(Animal).all()
	#return "This page will show all my animals"
	return render_template('animals.html', animals = animals)




#Create a new animal
@app.route('/animal/new/', methods=['GET','POST'])
def newAnimal():
	if request.method == 'POST':
		newAnimal = Animal(name = request.form['name'])
		session.add(newAnimal)
		session.commit()
		return redirect(url_for('showAnimals'))
	else:
		return render_template('newAnimal.html')
	#return "This page will be for making a new animal"

#Edit a animal
@app.route('/animal/<int:animal_id>/edit/', methods = ['GET', 'POST'])
def editAnimal(animal_id):
	editedAnimal = session.query(Animal).filter_by(id = animal_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedAnimal.name = request.form['name']
			return redirect(url_for('showAnimals'))
	else:
		return render_template('editAnimal.html', animal = editedAnimal)

	#return 'This page will be for editing animal %s' % animal_id

	    
#Delete a animal
@app.route('/animal/<int:animal_id>/delete/', methods = ['GET','POST'])
def deleteAnimal(animal_id):
	animalToDelete = session.query(Animal).filter_by(id = animal_id).one()
	if request.method == 'POST':
		session.delete(animalToDelete)
		session.commit()
		return redirect(url_for('showAnimals', animal_id = animal_id))
	else:
		return render_template('deleteAnimal.html',animal = animalToDelete)
	#return 'This page will be for deleting animal %s' % animal_id

#Show a animal pet
@app.route('/animal/<int:animal_id>/')
@app.route('/animal/<int:animal_id>/pet/')
def showPet(animal_id):
	animal = session.query(Animal).filter_by(id = animal_id).one()
	items = session.query(PetItem).filter_by(animal_id = animal_id).all()
	return render_template('pet.html', items = items, animal = animal)
	 #return 'This page is the pet for animal %s' % animal_id

#Create a new pet item
@app.route('/animal/<int:animal_id>/pet/new/',methods=['GET','POST'])
def newPetItem(animal_id):
	if request.method == 'POST':
		newItem = PetItem(name = request.form['name'], description = request.form['description'], gender = request.form['gender'], animal_id = animal_id)
		session.add(newItem)
		session.commit()
		
		return redirect(url_for('showPet', animal_id = animal_id))
	else:
		return render_template('newpetitem.html', animal_id = animal_id)

	return render_template('newpetitem.html', animal = animal)
	#return 'This page is for making a new pet item for animal %s' %animal_id

#Edit a pet item
@app.route('/animal/<int:animal_id>/pet/<int:pet_id>/edit', methods=['GET','POST'])
def editPetItem(animal_id, pet_id):
	editedItem = session.query(PetItem).filter_by(id = pet_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['description']:
			editedItem.description = request.form['description']
		if request.form['gender']:
			editedItem.gender = request.form['gender']
		session.add(editedItem)
		session.commit() 
		return redirect(url_for('showPet', animal_id = animal_id))
	else:
		
		return render_template('editpetitem.html', animal_id = animal_id, pet_id = pet_id, item = editedItem)

	
	#return 'This page is for editing pet item %s' % pet_id


#Delete a pet item
@app.route('/animal/<int:animal_id>/pet/<int:pet_id>/delete', methods = ['GET','POST'])
def deletePetItem(animal_id,pet_id):
	itemToDelete = session.query(PetItem).filter_by(id = pet_id).one() 
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		return redirect(url_for('showPet', animal_id = animal_id))
	else:
		return render_template('deletepetitem.html', item = itemToDelete)
	#return "This page is for deleting pet item %s" % pet_id


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
