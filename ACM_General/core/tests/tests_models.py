from django.test import TestCase

# Create your tests here.

class GenericModelTestCase(TestCase):
    class Meta:
        model = None
        model_data = None

    def setUp(self):
        model = self.Meta.model

        for item in model_data:
            for key in item:
                assert key in model._meta.get_all_field_names(),(
                'Your model_data dictonary contains a key which is not listed'
                'in the model fields. This key is {}'.format(key))

