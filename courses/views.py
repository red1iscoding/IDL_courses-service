from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from .models import Course, StudentCourse
from .serializers import CourseSerializer, StudentCourseSerializer

# Course Management
@api_view(['POST'])
def add_course(request):
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Course added successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_courses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CourseSerializer(course)
    return Response(serializer.data)

@api_view(['PUT'])
def update_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CourseSerializer(course, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Course updated successfully"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
    
    course.delete()
    return Response({"message": "Course deleted successfully"})

@api_view(['GET'])
def search_courses(request):
    search_query = request.GET.get('q', '')
    
    if not search_query:
        return Response({"error": "Please provide a search query parameter 'q'"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Search in name, instructor, or category
    courses = Course.objects.filter(
        models.Q(name__icontains=search_query) |
        models.Q(instructor__icontains=search_query) |
        models.Q(category__icontains=search_query)
    )
    
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

# Student-Course Association Management
@api_view(['POST'])
def enroll_student(request):
    serializer = StudentCourseSerializer(data=request.data)
    if serializer.is_valid():
        # Check if student is already enrolled in this course
        student_id = serializer.validated_data['student_id']
        course_id = serializer.validated_data['course'].id
        
        if StudentCourse.objects.filter(student_id=student_id, course_id=course_id).exists():
            return Response({"error": "Student is already enrolled in this course"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({"message": "Student enrolled successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def unenroll_student(request, enrollment_id):
    try:
        enrollment = StudentCourse.objects.get(id=enrollment_id)
    except StudentCourse.DoesNotExist:
        return Response({"error": "Enrollment not found"}, status=status.HTTP_404_NOT_FOUND)
    
    enrollment.delete()
    return Response({"message": "Student unenrolled successfully"})

@api_view(['GET'])
def get_course_enrollments(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
    
    enrollments = StudentCourse.objects.filter(course=course)
    serializer = StudentCourseSerializer(enrollments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_student_enrollments(request, student_id):
    enrollments = StudentCourse.objects.filter(student_id=student_id)
    serializer = StudentCourseSerializer(enrollments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_courses_with_students(request):
    # Get all courses with their enrolled students count
    courses = Course.objects.all()
    result = []
    
    for course in courses:
        student_count = StudentCourse.objects.filter(course=course).count()
        course_data = CourseSerializer(course).data
        course_data['enrolled_students_count'] = student_count
        result.append(course_data)
    
    return Response(result)