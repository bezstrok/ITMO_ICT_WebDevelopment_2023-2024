from rest_framework import serializers
from warriors_app import models


class WarriorSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Warrior
		fields = '__all__'


class WarriorDepthSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Warrior
		fields = '__all__'
		depth = 1


class WarriorSlug(serializers.ModelSerializer):
	skill = serializers.SlugRelatedField(slug_field='title', read_only=True, many=True)
	
	class Meta:
		model = models.Warrior
		fields = '__all__'


class ProfessionSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Profession
		fields = '__all__'


class ProfessionWithWarriorSerializer(serializers.ModelSerializer):
	warrior = WarriorSerializer(many=True, read_only=True)
	
	class Meta:
		model = models.Profession
		fields = ['title', 'description', 'warrior']


class ProfessionCreateSerializer(serializers.Serializer):
	title = serializers.CharField(max_length=120)
	description = serializers.CharField()
	
	# Переопределяем только его, потому что save более высокого уровня
	def create(self, validated_data):
		# validated_data - словарь, поэтому **
		prof_model_inst = models.Profession(**validated_data)
		prof_model_inst.save()
		return prof_model_inst
	
	def update(self, instance, validated_data):
		pass


class SkillSerializer(serializers.ModelSerializer):
	"""
	Можем использовать как для get, так и для post
	"""
	
	class Meta:
		model = models.Skill
		fields = '__all__'


class SkillWithWarrior(serializers.ModelSerializer):
	warrior = WarriorSerializer(many=True)
	
	class Meta:
		model = models.Skill
		fields = '__all__'


class WarriorProfessionSerializer(serializers.ModelSerializer):
	profession = ProfessionSerializer(many=False, read_only=True)
	
	class Meta:
		model = models.Warrior
		fields = '__all__'


class WarriorSkillSerializer(serializers.ModelSerializer):
	skill = SkillSerializer(many=True, read_only=True)
	
	class Meta:
		model = models.Warrior
		fields = '__all__'


class WarriorProfessionSkillSerializer(serializers.ModelSerializer):
	profession = ProfessionSerializer(many=False, read_only=True)
	skill = SkillSerializer(many=True, read_only=True)
	
	class Meta:
		model = models.Warrior
		fields = '__all__'
