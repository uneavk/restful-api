# 25. Екзамени:
# o Поля: id, subject_id, date, location, examiner.
#from _datetime import datetime
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exams.db'
db = SQLAlchemy(app)


par = reqparse.RequestParser()
par.add_argument("subject_id", type=int, required=False)
par.add_argument("date", type=str)
par.add_argument("location", type=int, required=False)
par.add_argument("examiner", type=str, required=False)

class ExamModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer)
    date = db.Column(db.String(255))
    location = db.Column(db.Integer)
    examiner = db.Column(db.String(255))

    def __init__(self, subject_id, date, location, examiner):
        self.subject_id = subject_id
        self.date = date
        self.location = location
        self.examiner = examiner

def abort_if_exam_doesnt_exist(exam_id):
    if not ExamModel.query.get(exam_id):
        abort(404, message=f"Exam {exam_id} doesn't exist")

class ExamResource(Resource):
    def get(self, exam_id=None):
        if exam_id :
            abort_if_exam_doesnt_exist(exam_id)
            exam = ExamModel.query.get(exam_id)
            return {
                "id": exam.id,
                "subject_id": exam.subject_id,
                "date": exam.date,
                "location": exam.location,
                "examiner": exam.examiner
            }
        else:
            exams = ExamModel.query.all()
            exam_data = [
                {
                    "id": exam.id,
                    "subject_id": exam.subject_id,
                    "date": exam.date,
                    "location": exam.location,
                    "examiner": exam.examiner
                }
                for exam in exams
            ]
            return '\n'.join(map(str, exam_data))

    def post(self):
        args = par.parse_args()
        new_exam = ExamModel(
            subject_id=args["subject_id"],
            date=args["date"],
            location=args["location"],
            examiner=args["examiner"],
        )
        db.session.add(new_exam)
        db.session.commit()
        return {
            "id": new_exam.id,
            "subject_id": new_exam.subject_id,
            "date": new_exam.date,
            "location": new_exam.location,
            "examiner": new_exam.examiner
        }, 201

    def delete(self, exam_id):
        abort_if_exam_doesnt_exist(exam_id)
        exam = ExamModel.query.get(exam_id)
        db.session.delete(exam)
        db.session.commit()
        return '', 204

    def put(self, exam_id):
        args = par.parse_args()
        exam = ExamModel.query.get(exam_id)
        if not exam:
            new_exam = ExamModel(
                subject_id=args["subject_id"],
                date=args["date"],
                location=args["location"],
                examiner=args["examiner"],
            )
            db.session.add(new_exam)
            db.session.commit()
            return {
                "id": new_exam.id,
                "subject_id": new_exam.subject_id,
                "date": new_exam.date,
                "location": new_exam.location,
                "examiner": new_exam.examiner
            }
        else:
            abort_if_exam_doesnt_exist(exam_id)
            exam.subject_id = args.get("subject_id", exam.subject_id)
            exam.date = args.get("date", exam.date)
            exam.location = args.get("location", exam.location)
            exam.examiner = args.get("examiner", exam.examiner)
            db.session.commit()
            return {
                "id": exam.id,
                "subject_id": exam.subject_id,
                "date": exam.date,
                "location": exam.location,
                "examiner": exam.examiner
            }, 201


api.add_resource(ExamResource, "/api/exams", "/api/exams/<int:exam_id>")


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        first_db = {
            1: {"subject_id": 23, "date": "2023-12-04 9:00", "location": 205, "examiner": "Ivanov S.M."},
            2: {"subject_id": 311, "date": "2023-12-05 9:00", "location": 232, "examiner": "Onotsky V.V"},
            3: {"subject_id": 24, "date": "2023-12-14 9:00", "location": 1, "examiner": "Korobova M.V."},
            4: {"subject_id": 14, "date": "2023-12-18 9:00", "location": 1, "examiner": "Ivokhin E.V."},
        }

        for exam_id, exam_info in first_db.items():
            new_exam = ExamModel(
                subject_id=exam_info["subject_id"],
                date=exam_info["date"],
                location=exam_info["location"],
                examiner=exam_info["examiner"]
            )
            db.session.add(new_exam)

        db.session.commit()
    app.run(debug=True, port=1103, host="127.0.0.1")
