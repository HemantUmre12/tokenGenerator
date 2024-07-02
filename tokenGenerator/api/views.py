from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .models.key_manager import key_manager


class KeyView(APIView):
    def post(self, request):
        key_id = key_manager.generate_key()
        return Response({"keyId": key_id}, status=status.HTTP_201_CREATED)

    def get(self, request):
        key_id = key_manager.get_key()
        if key_id is None:
            return Response(
                {"message": "No available keys at the moment."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response({"keyId": key_id}, status=status.HTTP_200_OK)


class KeyDetailView(APIView):
    def get(self, request, key_id):
        key_data = key_manager.get_key_info(key_id)
        if key_data is None:
            return Response(
                {"message": "No available key with the given ID."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(key_data, status=status.HTTP_200_OK)

    def delete(self, request, key_id):
        if key_id not in key_manager.keys:
            return Response(
                {"message": "No available key to delete with the given ID."},
                status=status.HTTP_404_NOT_FOUND,
            )

        key_manager.delete_key(key_id)
        return Response({"message": "Deleted successfully!"}, status=status.HTTP_200_OK)

    def put(self, request, key_id):
        if key_id not in key_manager.keys:
            return Response(
                {"message": "No available key to unblock with the given ID."},
                status=status.HTTP_404_NOT_FOUND,
            )

        key_manager.unblock_key(key_id)
        return Response(
            {"message": "Unblocked successfully!"}, status=status.HTTP_200_OK
        )


class KeepaliveView(APIView):
    def put(self, request, key_id):
        if key_id not in key_manager.keys:
            return Response(
                {"message": "No available key with the given ID."},
                status=status.HTTP_404_NOT_FOUND,
            )

        key_manager.keep_alive(key_id)
        return Response(
            {"message": "Extended the key's lifespan."}, status=status.HTTP_200_OK
        )
