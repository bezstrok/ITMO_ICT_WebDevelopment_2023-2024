from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from warriors_app import models, serializers


class WarriorAPIView(APIView):
	def get(self, request):
		warriors_query = models.Warrior.objects.all()
		warriors_serialized = serializers.WarriorSlug(
			warriors_query,
			many=True
		)
		return Response({'warriors': warriors_serialized.data}, status=200)


class WarriorAuthenticatedOnly(generics.ListAPIView):
	serializer_class = serializers.WarriorSlug
	queryset = models.Warrior.objects.all()
	permission_classes = [permissions.IsAuthenticated]


class WarriorWithProfessionView(generics.ListAPIView):
	serializer_class = serializers.WarriorProfessionSerializer
	queryset = models.Warrior.objects.all()


class WarriorWithSkillView(generics.ListAPIView):
	serializer_class = serializers.WarriorSkillSerializer
	queryset = models.Warrior.objects.all()


class WarriorRetrieveApiView(generics.RetrieveAPIView):
	serializer_class = serializers.WarriorProfessionSkillSerializer
	queryset = models.Warrior.objects.all()


class WarriorRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = serializers.WarriorSerializer
	queryset = models.Warrior.objects.all()


class WarriorCreateApiView(generics.CreateAPIView):
	# Если поле проходит через вложенный serializer, то оно не отображается
	# в полях. Аналогично и с depth
	serializer_class = serializers.WarriorSerializer
	queryset = models.Warrior.objects.all()


class ProfessionApiView(APIView):
	def get(self, request):
		profession_query = models.Profession.objects.all()
		profession_serializer = serializers.ProfessionWithWarriorSerializer(
			profession_query,
			many=True
		)
		return Response({'professions': profession_serializer.data}, status=200)


class ProfessionCreateView(APIView):
	def post(self, request):
		# Получаем из json данные под заголовком profession
		# Используем get, чтобы в случае если profession нет в словаре,
		# вернулось None
		prof_data = request.data.get('profession')
		prof_serializer = serializers.ProfessionCreateSerializer(data=prof_data)
		if prof_serializer.is_valid(raise_exception=True):
			prof_model_inst = prof_serializer.save()
		return Response({'Success': f'Profession {prof_model_inst.title} created'})


class SkillApiView(APIView):
	def get(self, request):
		skills_query = models.Skill.objects.all()
		skills_serialized = serializers.Skil(
			skills_query,
			many=True
		)
		return Response(skills_serialized.data)


class SkillCreateView(APIView):
	def post(self, request):
		skill_dict = request.data.get('skill')
		skill_serialized = serializers.SkillSerializer(data=skill_dict)
		if skill_serialized.is_valid(raise_exception=True):
			skill_obj = skill_serialized.save()
		return Response({'Success': f'Skill {skill_obj.title} created'})


class SkillWithWarrior(APIView):
	def get(self, request):
		skills_query = models.Skill.objects.all()
		skills_serialized = serializers.SkillWithWarrior(
			skills_query,
			many=True
		)
		return Response(skills_serialized.data)
