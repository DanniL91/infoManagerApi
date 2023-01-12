from rest_framework.response import Response
from rest_framework import status
from person.models import Person
from person.serializer import PersonSerializer, SearchPerson
from rest_framework.views import APIView
import logging
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests 


# Get an instance of a logger
logging.basicConfig(filename='info_manager.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

response_schema_dict = {
    "200": openapi.Response(description="Description",
        examples={
            "application/json": {
                "status": "200",
                "message": "Successful"
            }
        }
    ),
    "400": openapi.Response(description="Description",
        examples={
            "application/json": {
                "status": "400",
                "message": "Client Error"
            }
        }
    ),
    "500": openapi.Response(description="Description",
        examples={
            "application/json": {
                "status": "500",
                "message": "Server Error",
            }
        }
    ),
}

class PersonApiView(APIView, Exception):
    serializer_person = PersonSerializer
    
    @swagger_auto_schema(query_serializer=SearchPerson, operation_id='Search Person', responses=response_schema_dict)
    def get(self, request):
        try:
            documentType = request.GET.get('documentType')
            documentNumber = request.GET.get('documentNumber')
            if None in (documentType, documentNumber):
                person = Person.objects.all()
            else:
                person = Person.objects.filter(documentType__iexact=documentType, documentNumber__iexact=documentNumber)
            if person.exists():
                res = self.serializer_person(person , many=True)
                return Response({"status": "200", "data": res.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "Successful", "message": "NO_CONTENT"}, status=status.HTTP_204_NO_CONTENT)
        except (Person.DoesNotExist, AssertionError) as e:
            logger.info(str(e))
            return Response({"status": "204", "message": "NO_CONTENT"}, status=status.HTTP_204_NO_CONTENT)
        except (KeyError, requests.RequestException) as e:
            logger.info(str(e))
            return Response({"status": "400", "message":  str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.info(str(e))
            return Response({"status": "500", "message":  str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(request_body=PersonSerializer, operation_id='Create Person', responses=response_schema_dict)
    def post(self, request):
        try:
            serializer = self.serializer_person(data=request.data)
            documentType = request.data["documentType"]
            documentNumber = request.data["documentNumber"] 
            person = Person.objects.filter(documentType__iexact=documentType, documentNumber=documentNumber)
            if person.exists():
                return Response({"status": "204", "message": "Person Exist"}, status=status.HTTP_204_NO_CONTENT)
            else:
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": "201", "message": "Person created"}, status=status.HTTP_201_CREATED)
                else:
                    logger.warning({"message": serializer.errors})
                    raise PersonApiView
        except (PersonApiView) as e:
            logger.info(str(e))
            return Response({"status": "422", "message": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except (KeyError, requests.RequestException, AssertionError) as e:
            logger.info(str(e))
            return Response({"status": "400", "message":  str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.info(str(e))
            return Response({"status": "500", "message":  str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @swagger_auto_schema(request_body=PersonSerializer, operation_id='Update Person', responses=response_schema_dict)
    def put(self, request):
        try:
            documentType = request.data["documentType"]
            documentNumber = request.data["documentNumber"]        
            if None in (documentType, documentNumber):
                logger.info(str(e))
                return Response({"status": "Bad Request", "message": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                person = Person.objects.get(documentType__iexact=documentType, documentNumber=documentNumber)
                serializer = self.serializer_person(person, data=request.data, partial=True)
                if serializer.is_valid():
                    print("nuevo")
                    serializer.validated_data['first_name'] = request.data["first_name"] 
                    serializer.validated_data['second_name'] = request.data["second_name"] 
                    serializer.validated_data['lastName'] = request.data["lastName"] 
                    serializer.validated_data['hobbie'] = request.data["hobbie"] 
                    serializer.save()
                return Response({"status": "200", "message": "OK"}, status=status.HTTP_200_OK)
        except (Person.DoesNotExist):
            return Response({"status": "204", "message": "NO_CONTENT"}, status=status.HTTP_204_NO_CONTENT)
        except (KeyError, AssertionError) as e:
            logger.info(str(e))
            return Response({"status": "400", "message":  str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.info(str(e))
            return Response({"status": "500", "message":  str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




    @swagger_auto_schema(query_serializer=SearchPerson, operation_id='Delete Person', responses=response_schema_dict)
    def delete(self, request):
        try:
            documentType = request.GET.get('documentType')
            documentNumber = request.GET.get('documentNumber')       
            if None in (documentType, documentNumber):
                return Response({"status": "400", "message": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                person = Person.objects.get(documentType__iexact=documentType, documentNumber=documentNumber)
                person.delete()
                return Response({"status": "200", "message": "OK"}, status=status.HTTP_200_OK)
        except (Person.DoesNotExist):
            return Response({"status": "204", "message": "NO_CONTENT"}, status=status.HTTP_204_NO_CONTENT)
        except (KeyError, AssertionError) as e:
            logger.info(str(e))
            return Response({"status": "400", "message":  str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.info(str(e))
            return Response({"status": "500", "message":  str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
