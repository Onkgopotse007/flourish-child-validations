from edc_constants.constants import YES, NO
from edc_form_validators import FormValidator
from .form_validator_mixin import ChildFormValidatorMixin
from django.forms import ValidationError


class ChildTBScreeningFormValidator(ChildFormValidatorMixin, FormValidator):

    def clean(self):
        super().clean()

        required_fields = ['cough', 'fever', 'sweats', 'weight_loss']

        for field in required_fields:
            self.required_if(YES,
                             field=field,
                             field_required=f'{field}_duration')

        self.required_if(YES,
                         field='evaluated_for_tb',
                         field_required='clinic_visit_date')

        self.validate_other_specify(
            field='tb_tests',
            other_specify_field='other_test',
        )

        self.required_if('chest_xray',
                         field='tb_tests',
                         field_required='chest_xray_results')

        self.required_if('sputum_sample',
                         field='tb_tests',
                         field_required='sputum_sample_results')

        self.required_if('stool_sample',
                         field='tb_tests',
                         field_required='stool_sample_results')

        self.required_if('urine_test',
                         field='tb_tests',
                         field_required='urine_test_results')

        self.required_if('skin_test',
                         field='tb_tests',
                         field_required='skin_test_results')

        self.required_if('blood_test',
                         field='tb_tests',
                         field_required='blood_test_results')

        self.required_if(NO,
                         field='child_diagnosed_with_tb',
                         field_required='child_on_tb_preventive_therapy')

        self.required_if_true(condition=YES,
                              field='evaluated_for_tb',
                              field_required='tb_tests')

        self.field_cannot_be(field_1='child_diagnosed_with_tb',
                             field_2='child_on_tb_preventive_therapy',
                             field_one_condition=YES,
                             field_two_condition=YES)

    def field_cannot_be(self, field_1, field_2, field_one_condition,
                        field_two_condition):
        """Raises an exception based on the condition between field_1 and field_2
        values."""
        cleaned_data = self.cleaned_data
        field_1_value = cleaned_data.get(field_1)
        field_2_value = cleaned_data.get(field_2)

        if field_1_value == field_one_condition and field_2_value == field_two_condition:
            message = (f'Q.26 cannot be {field_two_condition} when '
                       f'Q.24 is {field_two_condition}.')
            raise ValidationError(message, code='message')
        return False
