from app.models.base import BaseModel
from datetime import datetime
from secrets import token_hex
from hashlib import sha512
from uuid import uuid4
from re import search, compile

import numpy as np

class User(BaseModel):

    async def get_all_users(self, course_id, semester, acedamic_year, **kwargs):
        try:
            cursor = self.app.mysql_conn.cursor(buffered=True)
            stmt = 'SELECT c.course_title AS course_name,\
                s.student_id AS student_id, s.first_name AS first_name, s.last_name AS last_name, \
                s.nickname AS nickname, s.gpax AS gpax, s.embedding AS embedded \
                FROM student s \
                LEFT JOIN studentincourse st ON s.student_id = st.student_id\
                LEFT JOIN course c ON st.course_id = c.course_id\
                WHERE c.course_id = %s AND st.semester = %s AND st.acedamic_year = %s'
            value = (course_id,semester,acedamic_year)
            cursor.execute(stmt,value)
            students = cursor.fetchall()
            if len(students) > 0:
                course = students[0][0]
                users = [
                    {
                        'student_id': user[1],
                        'student_first_name': user[2],
                        'student_last_name': user[3],
                        'student_nickname': user[4],
                        'gpax': user[5],
                        'embedded_face': np.loads(user[6]).tolist(),
                    }
                    for user in students
                ]
            else: 
                course = 'not found this course'
                users = []
            cursor.close()
            return {'status': 'success', 'course': course, 'student': users}
        except:
            try:
                cursor.close()
            except:
                pass
            return {'status': 'err'}

    async def save_face(self, first_name, last_name, nickname, gpax, student_id, face, **kwargs):
        try:
            face = np.array(face).dumps()
            cursor = self.app.mysql_conn.cursor(buffered=True)
            stmt = 'INSERT INTO student (student_id, first_name, last_name,\
                nickname, gpax, embedding)\
                VALUES (%s,%s,%s,%s,%s,%s)'
            value = (student_id, first_name, last_name, nickname, gpax, face)
            cursor.execute(stmt,value)
            self.app.mysql_conn.commit()
            cursor.close()
            return {'status': 'success.'}
        except:
            try:
                cursor.close()
            except:
                pass
            return {'status': 'err'}

    async def get_all_courses(self, semester, acedamic_year, **kwargs):
        try:
            cursor = self.app.mysql_conn.cursor(buffered=True)
            stmt = 'SELECT DISTINCT c.course_id, c.course_title FROM course c \
                LEFT JOIN studentincourse st ON c.course_id = st.course_id\
                WHERE st.semester = %s AND st.acedamic_year = %s'
            value = (semester, acedamic_year)
            cursor.execute(stmt,value)
            courses = [
                {
                    'course_id': course[0],
                    'course_name': course[1],
                }
                for course in cursor.fetchall()
            ]
            cursor.close()
            return {'status': 'success', 'courses': courses}
        except:
            try:
                cursor.close()
            except:
                pass
            return {'status': 'err'}
    
    async def add_student_in_course(self, course_id, student_id, semester, acedamic_year, **kwargs):
        try:
            cursor = self.app.mysql_conn.cursor(buffered=True)
            stmt = 'SELECT count(*) FROM studentincourse WHERE course_id = %s AND student_id = %s\
                 AND semester = %s AND acedamic_year = %s'
            value = (course_id, student_id, semester, acedamic_year)
            cursor.execute(stmt, value)
            if cursor.fetchone()[0]:
                cursor.close()
                reason = 'student id: '+str(student_id)+' is in course: '+str(course_id)+' semester: '+str(semester)+' acedamic year: '+str(acedamic_year) +' already'
                return {'status': 'err',
                        'reason': reason }
            else:
                stmt = 'SELECT count(*) FROM course WHERE course_id = %s'
                value = (course_id,)
                cursor.execute(stmt, value)
                if cursor.fetchone()[0]:
                    stmt = 'SELECT count(*) FROM student WHERE student_id = %s'
                    value = (student_id,)
                    cursor.execute(stmt, value)
                    if cursor.fetchone()[0]:
                        stmt = 'INSERT INTO studentincourse (course_id, student_id, semester, acedamic_year)\
                            VALUES (%s,%s,%s,%s)'
                        value = (course_id, student_id, semester, acedamic_year)
                        cursor.execute(stmt, value)
                        self.app.mysql_conn.commit()
                        cursor.close()
                        reason = 'add student id: '+str(student_id)+' in course '+str(course_id)+' semester: '+str(semester)+' acedamic year: '+str(acedamic_year)
                        return {'status': 'success.',
                                'reason': reason }
                    else:
                        cursor.close()
                        reason = 'can not found student id: ' + str(student_id)
                        return {'status': 'err',
                                'reason': reason }
                else:
                    cursor.close()
                    return {'status': 'err',
                            'reason': 'can not found course id' }
        except:
            try:
                cursor.close()
            except:
                pass
            return {'status': 'err'}

    async def add_student_attendants(self, course_id, student_id, semester, acedamic_year, date, **kwargs):
        try:
            cursor = self.app.mysql_conn.cursor(buffered=True)
            stmt = 'SELECT count(*) FROM studentincourse WHERE course_id = %s AND student_id = %s\
                 AND semester = %s AND acedamic_year = %s'
            value = (course_id, student_id, semester, acedamic_year)
            cursor.execute(stmt, value)
            if cursor.fetchone()[0]:
                stmt = 'SELECT count(*) FROM course WHERE course_id = %s'
                value = (course_id,)
                cursor.execute(stmt, value)
                if cursor.fetchone()[0]:
                    stmt = 'SELECT count(*) FROM student WHERE student_id = %s'
                    value = (student_id,)
                    cursor.execute(stmt, value)
                    if cursor.fetchone()[0]:
                        stmt = 'SELECT count(*) FROM attendants WHERE course_id = %s AND student_id = %s AND semester = %s AND acedamic_year = %s AND date = %s'
                        value = (course_id, student_id, semester, acedamic_year, date)
                        cursor.execute(stmt, value)
                        if cursor.fetchone()[0]:
                            stmt = 'INSERT INTO attendants (course_id, student_id, semester, acedamic_year, date)\
                                VALUES (%s,%s,%s,%s,%s)'
                            value = (course_id, student_id, semester, acedamic_year, date)
                            cursor.execute(stmt, value)
                            self.app.mysql_conn.commit()
                            cursor.close()
                            reason = 'check student id: '+str(student_id)+' in course '+str(course_id)+' semester: '+str(semester)+' acedamic year: '+str(acedamic_year)+' day: '+str(date)
                            return {'status': 'success.',
                                    'reason': reason }
                        else:
                            cursor.close()
                            reason = 'student id: ' + str(student_id) + ' is check in already '
                            return {'status': 'err',
                                    'reason': reason }
                    else:
                        cursor.close()
                        reason = 'can not found student id: ' + str(student_id)
                        return {'status': 'err',
                                'reason': reason }
                else:
                    cursor.close()
                    return {'status': 'err',
                            'reason': 'can not found course id' }
            else:
                cursor.close()
                reason = 'student id: '+str(student_id)+' is not in course: '+str(course_id)+' semester: '+str(semester)+' acedamic year: '+str(acedamic_year)
                return {'status': 'err',
                        'reason': reason }
        except:
            try:
                cursor.close()
            except:
                pass
            return {'status': 'err'}

    async def get_attendants(self, course_id, semester, acedamic_year, date,**kwargs):
        try:
            cursor = self.app.mysql_conn.cursor(buffered=True)
            stmt = 'SELECT DISTINCT * FROM student s \
                LEFT JOIN attendants at ON at.student_id = s.student_id\
                WHERE at.course_id = %s AND at.semester = %s AND at.acedamic_year = %s AND at.date = %s'
            value = (course_id, semester, acedamic_year, date)
            cursor.execute(stmt,value)
            students = cursor.fetchall()
            if len(students) > 0:
                users = [
                    {
                        'student_id': user[0],
                        'student_first_name': user[1],
                        'student_last_name': user[2],
                        'student_nickname': user[3],
                        'gpax': user[4],
                        'embedded_face': np.loads(user[5]).tolist(),
                    }
                    for user in students
                ]
            else: 
                course = 'not found student'
                users = []
            cursor.close()
            return {'status': 'success', 'student': users}
        except:
            try:
                cursor.close()
            except:
                pass
            return {'status': 'err'}