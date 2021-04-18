from app.controllers.base import Controller
from app.models.user import User

class UserController(Controller):

    async def get_face_students(self, request):
        try:
            payload = await request.json()
            try:
                if payload is not None:
                    print('can get payload')
            except (NameError, AttributeError):
                print('not found payload')
            response = await User(request.app).get_all_users(**payload)
            await self.write(request, self.json_response(response))
        except:
            response = {'status': 'Bad Request.',
                        'reason': 'Controller rejected. Please check input.'}
            await self.write(request, self.json_response(response))

    async def add_face_students(self, request):
        try:
            payload = await request.json()
            try:
                if payload is not None:
                    print('can get payload')
            except (NameError, AttributeError):
                print('not found payload')
            response = await User(request.app).save_face(**payload)
            await self.write(request, self.json_response(response))
        except:
            response = {'status': 'Bad Request.',
                        'reason': 'Controller rejected. Please check input.'}
            await self.write(request, self.json_response(response))
            
    async def get_all_courses(self, request):
        try:
            payload = await request.json()
            try:
                if payload is not None:
                    print('can get payload')
            except (NameError, AttributeError):
                print('not found payload')
            response = await User(request.app).get_all_courses(**payload)
            await self.write(request, self.json_response(response))
        except:
            response = {'status': 'Bad Request.',
                        'reason': 'Controller rejected. Please check input.'}
            await self.write(request, self.json_response(response))

    async def add_student_in_course(self, request):
        try:
            payload = await request.json()
            try:
                if payload is not None:
                    print('can get payload')
            except (NameError, AttributeError):
                print('not found payload')
            list_response = []
            term = payload['semester']
            year = payload['acedamic_year']
            for student in payload['students']:
                response = await User(request.app).add_student_in_course(payload['course_id'],student['student_id'],term,year)
                list_response.append(response)
                if response['status'] ==  'err' and response['reason'] == 'can not found course id':
                    break
            await self.write(request, self.json_response({'list_response':list_response}))
        except:
            response = {'status': 'Bad Request.',
                        'reason': 'Controller rejected. Please check input.'}
            await self.write(request, self.json_response(response))

    async def add_student_attendants(self, request):
        try:
            payload = await request.json()
            try:
                if payload is not None:
                    print('can get payload')
            except (NameError, AttributeError):
                print('not found payload')
            list_response = []
            term = payload['semester']
            year = payload['acedamic_year']
            date = payload['date']
            for student in payload['students']:
                response = await User(request.app).add_student_attendants(payload['course_id'],student['student_id'],term,year,date)
                list_response.append(response)
                if response['status'] ==  'err' and response['reason'] == 'can not found course id':
                    break
            await self.write(request, self.json_response({'list_response':list_response}))
        except:
            response = {'status': 'Bad Request.',
                        'reason': 'Controller rejected. Please check input.'}
            await self.write(request, self.json_response(response))

    async def get_attendants(self, request):
        try:
            payload = await request.json()
            try:
                if payload is not None:
                    print('can get payload')
            except (NameError, AttributeError):
                print('not found payload')
            response = await User(request.app).get_attendants(**payload)
            await self.write(request, self.json_response(response))
        except:
            response = {'status': 'Bad Request.',
                        'reason': 'Controller rejected. Please check input.'}
            await self.write(request, self.json_response(response))
