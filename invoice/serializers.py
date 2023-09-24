from .models import (
    Invoice,
    Invoice_details

)

from rest_framework import serializers


class Invoice_details_serializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice_details
        exclude = ["created_on","updated_on","invoice","id","slug_field"]

    

class Invoice_serializer(serializers.ModelSerializer):
    invoice_details = Invoice_details_serializer(many=True)
    class Meta:
        model = Invoice
        fields = ["date","invoice_details","slug_field"]


    def create(self,validated_data):
        invoice_details_data = validated_data.pop('invoice_details')

        invoice = Invoice.objects.create(**validated_data)


        for invoice_detail_data in invoice_details_data:
            Invoice_details.objects.create(invoice=invoice, **invoice_detail_data)

        return invoice
    
    def update(self, instance, validated_data):
        invoice_details_data = validated_data.pop('invoice_details')

        # Update the Invoice instance with the new data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save the updated Invoice instance
        instance.save()

        # Update or create related Invoice_details instances
        for invoice_detail_data in invoice_details_data:
            # Extract or create the Invoice_details instance related to this Invoice
            invoice_detail, created = Invoice_details.objects.update_or_create(
                invoice=instance,  # Assuming you have a ForeignKey named 'invoice' in Invoice_details
                defaults=invoice_detail_data
            )

        return instance


class List_invoice_serializer(serializers.ModelSerializer):
    invoice_details = Invoice_details_serializer(many=True)
    customer_name = serializers.SerializerMethodField()
    class Meta:
        model = Invoice
        fields = ["customer_name","date","invoice_details","slug_field"]

    
    def get_customer_name(self,obj):
        return obj.customer_name.username
    

   



    