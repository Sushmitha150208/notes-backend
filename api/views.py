from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Note
from .serializers import NoteSerializer


# REGISTER API
@api_view(["POST"])
def register(request):

    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"message": "Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"message": "Username already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    User.objects.create_user(
        username=username,
        password=password
    )

    return Response(
        {"message": "Registered successfully"},
        status=status.HTTP_201_CREATED
    )


# LOGIN API
@api_view(["POST"])
def login(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(
        username=username,
        password=password
    )

    if user is not None:
        return Response({
            "message": "Login successful",
            "user_id": user.id,
            "username": user.username
        })

    return Response(
        {"message": "Invalid username or password"},
        status=status.HTTP_401_UNAUTHORIZED
    )


# GET ALL NOTES / CREATE NOTE
@api_view(["GET", "POST"])
def notes(request):

    # GET NOTES
    if request.method == "GET":

        username = request.GET.get("username")

        if not username:
            return Response(
                {"message": "Username is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        notes = Note.objects.filter(user=user)

        serializer = NoteSerializer(notes, many=True)

        return Response(serializer.data)


    # CREATE NOTE
    if request.method == "POST":

        username = request.data.get("username")
        title = request.data.get("title")
        description = request.data.get("description")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        note = Note.objects.create(
            user=user,
            title=title,
            description=description
        )

        serializer = NoteSerializer(note)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


# EDIT / DELETE NOTE
@api_view(["PUT", "DELETE"])
def note_detail(request, id):

    try:
        note = Note.objects.get(id=id)
    except Note.DoesNotExist:
        return Response(
            {"message": "Note not found"},
            status=status.HTTP_404_NOT_FOUND
        )


    # EDIT
    if request.method == "PUT":

        note.title = request.data.get("title")
        note.description = request.data.get("description")

        note.save()

        serializer = NoteSerializer(note)

        return Response(serializer.data)


    # DELETE
    if request.method == "DELETE":

        note.delete()

        return Response({
            "message": "Note deleted successfully"
        })