from rest_framework import generics, status
from rest_framework.response import Response
from .models import User, Incident
from .serializers import UserSerializer, IncidentSerializer
import requests
import json
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.exceptions import ValidationError

class GetInfofromPin(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        pincode = self.kwargs['pincode']
        endpoint = f'https://api.postalpincode.in/pincode/{pincode}'
        response = requests.get(endpoint)

        if response.status_code == 200:
            pincode_information = json.loads(response.text)
            if pincode_information and isinstance(pincode_information, list):
                city = pincode_information[0].get('PostOffice', [])[0].get('District', '')
                state = pincode_information[0].get('PostOffice', [])[0].get('State', '')
                country = pincode_information[0].get('PostOffice', [])[0].get('Country', '')
                return Response({'city': city,'state':state, 'country': country}, status=status.HTTP_200_OK)
        return Response({'detail': 'Pincode not found'}, status=status.HTTP_404_NOT_FOUND)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Override the post method to handle pin code and auto-populate City and Country
    def post(self, request, *args, **kwargs):
        # Extract the pin code from the request data
        pincode = request.data.get('pincode')

        # Make an AJAX request to GetInfofromPin view to fetch city and country information
        response = requests.get(f'http://127.0.0.1:8000/api/pincode/{pincode}/')

        if response.status_code == 200:
            data = response.json()
            # Update the request data with the fetched City and Country
            request.data['city'] = data.get('city', '')
            request.data['state'] = data.get('state', '')
            request.data['country'] = data.get('country', '')

            # Continue with user creation
            response = super(UserCreateView, self).post(request, *args, **kwargs)

            if response.status_code == 201:
                # User created successfully
                return Response({'detail': 'User created successfully'}, status=status.HTTP_201_CREATED)
            else:
                # Handle other response status codes or errors if needed
                return response
        else:
            return Response({'detail': 'Failed to fetch pincode information'}, status=response.status_code)

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                return [user]  # Return a list containing the single user
            except User.DoesNotExist:
                raise Http404("User does not exist")

        # If user_id is not provided, return all users
        return User.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        # Extract user_id from the request data
        user_id = request.query_params.get('user_id')

        if user_id is None:
            # If user_id is not provided, return a validation error response
            raise ValidationError({'user_id': ['User ID must be provided for update.']})

        # Get the user object based on user_id
        instance = get_object_or_404(User, pk=user_id)

        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'User updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()

    def destroy(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')

        if user_id is None:
            # If user_id is not provided, return a validation error response
            return Response({'detail': 'User ID must be provided for deletion.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            # If the user with the provided user_id does not exist, return a not found response
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Perform the deletion
        instance.delete()

        return Response({'detail': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class IncidentCreateView(generics.CreateAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

    def create(self, request, *args, **kwargs):
        # Check if the reporter exists based on their user ID (assuming it's provided in the request)
        reporter_id = request.data.get('reporter_id')
        print("reporter_id:::::::::::::::", reporter_id)
        try:
            reporter_name = User.objects.get(pk=reporter_id)
            print("reporter:::::::::::", reporter_name)
            print("user exists")
        except User.DoesNotExist:
            # Log a message if the reporter does not exist
            return Response({'detail': 'Reporter not found'}, status=status.HTTP_404_NOT_FOUND)

          # Add reporter_name to the request data as 'reporter'
        request.data['reporter'] = reporter_name.first_name + " " + reporter_name.last_name

         # Use the modified request data to create the incident
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Create the incident record (without saving it to the database)
            incident = serializer.save()

            # Since reporter is now assigned, you don't need to update reporter_name
            print("you are here")
            return Response({'detail': 'Incident created successfully'}, status=status.HTTP_201_CREATED)
        else:
            print("serializer not valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        


class IncidentListView(generics.ListAPIView):
    serializer_class = IncidentSerializer

    def get_queryset(self):
        queryset = Incident.objects.all()
        userid = self.request.query_params.get('user_id')
        incidentid = self.request.query_params.get('incident_id')

        try:
            # Create an initial queryset that includes all incidents
            if userid:
                queryset = queryset.filter(reporter_id=userid)
            if incidentid:
                queryset = queryset.filter(incident_id=incidentid)
        except Exception as e:
            return Response({'detail': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IncidentUpdateView(generics.UpdateAPIView):
    serializer_class = IncidentSerializer

    def get_object(self):
        incident_id = self.request.query_params.get('incident_id')
        try:
            # Assuming your model has a field named 'incident_id'
            return Incident.objects.get(incident_id=incident_id)
        except Incident.DoesNotExist:
            return None

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance is None:
            return Response({'detail': 'Incident not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the incident is closed before allowing the update
        if instance.status == 'Closed':
            return Response({'detail': 'Closed incidents cannot be edited.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Incident updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class IncidentDeleteView(generics.DestroyAPIView):
    serializer_class = IncidentSerializer

    def get_object(self):
        incident_id = self.request.query_params.get('incident_id')
        try:
            return Incident.objects.get(incident_id=incident_id)
        except Incident.DoesNotExist:
            return None

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance is None:
            return Response({'detail': 'Incident not found'}, status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response({'detail': 'Incident deleted successfully'}, status=status.HTTP_204_NO_CONTENT)