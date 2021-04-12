from app.controllers.users_controller import UserController
from aiohttp_cors import setup, ResourceOptions


def map_routes(app):

    cors = setup(app, defaults={
        '*': ResourceOptions(
            allow_credentials=True,
            expose_headers='*',
            allow_headers='*',
        )
    })

    user_controller = UserController()

    resource = app.router.add_resource('/addFace', name='add_face')
    resource.add_route('POST', user_controller.add_face_students)

    resource = app.router.add_resource('/fetchStudent', name='student_data')
    resource.add_route('POST', user_controller.get_face_students)

    resource = app.router.add_resource('/fetchCourse', name='course_data')
    resource.add_route('POST', user_controller.get_all_courses)

    resource = app.router.add_resource('/addStudentInCourse', name='add_student_in_course')
    resource.add_route('POST', user_controller.add_student_in_course)

    resource = app.router.add_resource('/addAttendants', name='add_student_attendants')
    resource.add_route('POST', user_controller.add_student_attendants)
    
    resource = app.router.add_resource('/fetchAttendants', name='student_attendants')
    resource.add_route('POST', user_controller.get_attendants)

    for route in app.router.routes():
        cors.add(route)
