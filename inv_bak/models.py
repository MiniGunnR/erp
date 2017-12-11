from django.db import models

from utils.models import Timestamped


class LC(Timestamped):
    """
    This model saves LC information.
    """
    date = models.DateField()
    number = models.CharField(max_length=50)
    spinning_mill = models.CharField(max_length=50)

    def __str__(self):
        return self.number

    class Meta:
        verbose_name_plural = "LC"


KG = 'kg'

UNIT_CHOICES = [
    (KG, 'KG'),
]


class LCItem(models.Model):
    """
    This model contains the items issued in an LC.
    """
    lc = models.ForeignKey(
        LC,
        on_delete=models.CASCADE
    )
    count = models.CharField(max_length=20)
    composition = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(
        max_length=2,
        choices=UNIT_CHOICES,
        default=KG
    )
    style = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=100, blank=True)

    yarn_rcv = models.PositiveIntegerField(default=0)
    yarn_bal = models.PositiveIntegerField(default=0)
    yarn_dlv = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{lc} - Count: {count}, Comp: {comp}".format(
            lc=self.lc.number, count=self.count, comp=self.composition
        )

    def available_to_receive(self):
        """
        Available amount to be received.
        """
        return self.quantity - self.yarn_rcv

    def can_receive_yarn(self):
        """
        Returns true if current item have not fully been received.
        """
        return self.available_to_receive() > 0

    def receive_yarn(self, amount):
        """
        Receives yarn and saves it to the model.
        """
        if self.can_receive_yarn():
            if self.available_to_receive() >= amount:
                self.yarn_rcv += amount
                self.yarn_bal += amount
                if self.yarn_bal < 0:
                    return "Yarn Balance cannot be zero. Please check the current transaction for any errors."
                self.save()
            else:
                raise ArithmeticError("Amount to receive cannot be more than amount available.")
        else:
            raise ArithmeticError("Quantity issued on LC have already been received.")

    def edit_receive(self, old_amount, new_amount):
        """
        Edits the receive transaction.
        """
        self.yarn_rcv -= old_amount
        self.yarn_bal -= old_amount
        # return the next line to return original error messages
        return self.receive_yarn(new_amount)

    def deliver_yarn(self, amount):
        """
        Adds amount to the yarn_dlv field and subtracts the same from yarn_bal field.
        If amount is greater than balance then shows an error message.
        """
        if amount > self.yarn_bal:
            return "Amount to deliver is greater than current yarn balance."
        self.yarn_bal -= amount
        self.yarn_dlv += amount
        self.save()

    def edit_deliver(self, old_amount, new_amount):
        """
        Edits the deliver transaction.
        """
        self.yarn_bal += old_amount
        self.yarn_dlv -= old_amount
        return self.deliver_yarn(new_amount)


class YarnRcv(Timestamped):
    lc_item = models.ForeignKey(LCItem, on_delete=models.CASCADE)
    date = models.DateField()
    challan_no = models.CharField(max_length=20)
    lot = models.CharField(max_length=20)
    quantity_rcv = models.PositiveIntegerField("Quantity Received")

    def __str__(self):
        return "{lc_item} - challan: {challan}, lot: {lot}".format(
            lc_item=self.lc_item, challan=self.challan_no, lot=self.lot
        )

    class Meta:
        verbose_name_plural = "Yarn Rcv"

    def save(self, *args, **kwargs):
        # if object is created
        if self.pk is None:
            self.lc_item.receive_yarn(self.quantity_rcv)
        # if object is updated
        else:
            prev_quantity_rcv = YarnRcv.objects.get(id=self.pk).quantity_rcv
            # if previous qty and current qty is not the same
            if prev_quantity_rcv != self.quantity_rcv:
                self.lc_item.edit_receive(prev_quantity_rcv, self.quantity_rcv)
        super().save(*args, **kwargs)
