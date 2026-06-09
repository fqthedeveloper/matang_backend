from django.db.models import Count
from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Member
from .serializers import MemberSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

# =====================================================
# DASHBOARD
# =====================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):

    total_members = Member.objects.count()

    male_members = Member.objects.filter(
        gender="Male"
    ).count()

    female_members = Member.objects.filter(
        gender="Female"
    ).count()

    latest_members = Member.objects.order_by(
        "-id"
    )[:10]

    latest_serializer = MemberSerializer(
        latest_members,
        many=True
    )

    return Response({
        "total_members": total_members,
        "male_members": male_members,
        "female_members": female_members,
        "latest_members": latest_serializer.data
    })


# =====================================================
# MEMBER LIST
# =====================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def member_list(request):

    members = Member.objects.all().order_by(
        "-id"
    )

    serializer = MemberSerializer(
        members,
        many=True
    )

    return Response(serializer.data)


# =====================================================
# MEMBER DETAILS
# =====================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def member_detail(request, pk):

    try:

        member = Member.objects.get(
            id=pk
        )

    except Member.DoesNotExist:

        return Response(
            {
                "error": "Member not found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = MemberSerializer(
        member
    )

    return Response(
        serializer.data
    )


# =====================================================
# CREATE MEMBER
# =====================================================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_member(request):

    serializer = MemberSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# =====================================================
# UPDATE MEMBER
# =====================================================

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_member(request, pk):

    try:

        member = Member.objects.get(
            id=pk
        )

    except Member.DoesNotExist:

        return Response(
            {"error":"Member not found"},
            status=404
        )

    serializer = MemberSerializer(
        member,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():

        serializer.save()

        return Response(
            serializer.data
        )

    return Response(
        serializer.errors,
        status=400
    )


# =====================================================
# DELETE MEMBER
# =====================================================

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_member(request, pk):

    try:

        member = Member.objects.get(
            id=pk
        )

    except Member.DoesNotExist:

        return Response(
            {
                "error": "Member not found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    member.delete()

    return Response({
        "message": "Member deleted successfully"
    })


# =====================================================
# SEARCH MEMBER
# =====================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_member(request):

    keyword = request.GET.get(
        "q",
        ""
    )

    members = Member.objects.filter(

        Q(full_name__icontains=keyword) |
        Q(mobile__icontains=keyword) |
        Q(father_name__icontains=keyword) |
        Q(native_place__icontains=keyword) |
        Q(occupation__icontains=keyword)

    ).order_by("-id")

    serializer = MemberSerializer(
        members,
        many=True
    )

    return Response(
        serializer.data
    )


# =====================================================
# MALE MEMBERS
# =====================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def male_members(request):

    members = Member.objects.filter(
        gender="Male"
    )

    serializer = MemberSerializer(
        members,
        many=True
    )

    return Response(
        serializer.data
    )


# =====================================================
# FEMALE MEMBERS
# =====================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def female_members(request):

    members = Member.objects.filter(
        gender="Female"
    )

    serializer = MemberSerializer(
        members,
        many=True
    )

    return Response(
        serializer.data
    )