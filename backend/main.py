from flask import Flask, jsonify ,request
from config import app, db
from models import Contact

@app.route("/contacts" ,methods=["GET"])
def get_contacts():
  contacts=Contact.query.all()
  json_contacts = list(map(lambda x:x.to_json(),contacts))
  return jsonify({"contacts":json_contacts}),200

@app.rout("/create" ,methods=["POST"])
def craete_contact():
  first_name =request.json.get("firstname")
  last_name =request.json.get("lastName")
  email =request.json.get("email")
  
  if not first_name or not last_name or not email:
    return (
      jsonify({"massage ":"You must Include the details"}),400,
      )

  new_contact = Contact(first_name=first_name, last_name=last_name,email=email)
  
  try:
    db.session.add(new_contact)
    db.session.commit()
  except Exception as e:
    return jsonify({"message": str(e)}), 400
  return jsonify({"message" : "User craeted"}), 201


@app.route("/update_contact<int:user_id>" )
def update_contact(user_id):
  contact = Contact.query.get(user_id)
  if not contact:
    return jsonify({"massage":"user Not Found"}),404
  
  data = request.json
  contact.first_name =data.get("firstName", contact.first_name)
  contact.last_name =data.get("LastName", contact.last_name)
  contact.email =data.get("Email", contact.email)
  
  db.session.commit()
  
  return jsonify({"massage":"Usr updated"}), 200


@app.route("/delete_contact<int:user_id>" methods=["DELETE"])
def delete_contact(user_id):
  contact = Contact.query.get(user_id)
  if not contact:
    return jsonify({"massage":"user Not Found"}),404
  
  db.session.delete(contact)
  db.session.commit()

if __name__ =="__main__":
  with app.app_context():
    db.create_all()
  app.run(debug=True)