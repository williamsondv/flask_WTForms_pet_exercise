"""Adopt application."""

from flask import Flask, render_template, redirect, request, flash
from models import Pet, db, connect_db
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/pets'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

app.app_context().push()
connect_db(app)
db.create_all()

@app.route('/', methods=['GET', 'POST'])
def root():
    

    pets = Pet.query.all()
    return render_template("homepage.html", pets=pets)

@app.route('/add', methods=["GET", "POST"])
def add_pet():
    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        age = form.age.data
        photo = form.img_url.data
        notes = form.notes.data
        available = form.available.data

        if photo != None and photo != "":
            pet = Pet(name=name, species=species, img_url=photo, age=age, notes=notes, available=available)
        else:
             pet = Pet(name=name, species=species, age=age, notes=notes, available=available)

        db.session.add(pet)
        db.session.commit()
        flash(f"Added {name} to list of pets!")
        return redirect('/')
    else: 
        return render_template("add_pet.html", form = form)


@app.route('/<int:pet_id>', methods=["GET", "POST"])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.img_url = form.img_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        flash(f"{pet.name} information updated!")
        return redirect("/")

    else:
        return render_template("edit_pet.html", pet = pet, form = form)
    
@app.route('/delete/<int:pet_id>', methods=["GET","POST"])
def delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()
    flash(f"{pet.name} has been removed!")
    return redirect('/')