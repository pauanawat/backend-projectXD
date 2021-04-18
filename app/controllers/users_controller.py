from app.controllers.base import Controller
from app.models.user import User
from datetime import date
from datetime import datetime

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
            year = payload['academic_year']
            time_start = payload['start_time']
            time_end = payload['end_time']
            for student in payload['students']:
                response = await User(request.app).add_student_in_course(payload['course_id'],student['student_id'],term,year,time_start,time_end)
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
            list_response = dict()
            term = payload['semester']
            year = payload['academic_year']
            if 'date' in payload.keys() :
                today = payload['date']
                current_time = ''
                is_re_check = True
            else:
                day = date.today()
                today = day.strftime("%Y-%m-%d")

                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")

                is_re_check = False

            success = []
            not_found_student = []
            not_in_course = []
            check_already = []
            is_in_time = True
            is_found_course = True
            for student in payload['students']:
                response = await User(request.app).add_student_attendants(payload['course_id'],student['student_id'],term,year,today,current_time,is_re_check)
                if response['status'] ==  'success.' :
                    success.append(student['student_id'])
                elif response['status'] ==  'err' :
                    print('student_id:',student['student_id'],'has error in sql')
                elif response['status'] ==  'err1' :
                    ### not found course
                    is_found_course = False
                    is_in_time = False
                    break
                elif response['status'] ==  'err2' :
                    not_found_student.append(student['student_id'])
                elif response['status'] ==  'err3' :
                    not_in_course.append(student['student_id'])
                elif response['status'] ==  'err4' :
                    check_already.append(student['student_id'])
                elif response['status'] ==  'err5' :
                    ### not found course
                    is_in_time = False
                    break
            if is_found_course and is_in_time:
                list_response['success'] = success
                list_response['check_already'] = check_already
                list_response['not_in_course'] = not_in_course
                list_response['not_found_student'] = not_found_student
            else:
                list_response['success'] = []
                list_response['check_already'] = []
                list_response['not_in_course'] = []
                list_response['not_found_student'] = []
            list_response['is_in_time'] = is_in_time
            list_response['is_found_course'] = is_found_course
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
