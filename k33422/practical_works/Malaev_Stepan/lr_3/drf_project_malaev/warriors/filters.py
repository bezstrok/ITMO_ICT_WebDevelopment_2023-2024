import django.db.models as dj_models
from django_filters import rest_framework as filters
from warriors_app import models


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
	pass


class WarriorNameFilter(filters.FilterSet):
	skill__in = CharFilterInFilter(field_name='skill__title', lookup_expr='in').distinct
	
	all_skill_levels_gt = filters.NumberFilter(field_name='warrior_skill', method='filter_all_skill_levels_gt')
	
	class Meta:
		model = models.Warrior
		fields = {'level': ['gt', 'lt']}
	
	def filter_all_skill_levels_gt(self, queryset, name, value):
		if value:
			queryset = queryset.annotate(
				num_skills=dj_models.Count(name)
			).annotate(
				num_skills_gt_value=dj_models.Count('warrior_skill', filter=Q(warrior_skill__level__gt=value))
			).filter(
				num_skills=dj_models.F('num_skills_gt_value')
			)
		return queryset
	
	@property
	def qs(self):
		return super(WarriorNameFilter, self).qs
