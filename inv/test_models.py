from django.test import TestCase

from .models import LC, LCItem, YarnRcv


class LCItemTests(TestCase):

    def setUp(self):
        lc = LC.objects.create(date="2017-12-08", number="0987654321", spinning_mill="Demo Spinning Mill")
        obj = LCItem.objects.create(
            lc=lc,
            count='24/s',
            composition='100% Cotton',
            quantity=1000,
            unit='kg',
            style_no='Demo Style',
            color='Demo Color',
        )

    def test_lcitem_methods(self):
        """
        Test all the different outcomes of the LCItem methods.
        """
        lc = LC.objects.get(number="0987654321")
        obj = LCItem.objects.get(lc=lc)
        # Available 1000
        self.assertEqual(obj.available_to_receive(), 1000)
        # Error when amount is more than available
        self.assertEqual(obj.receive_yarn(1200), "Amount to receive cannot be more than amount available.")
        obj.yarn_rcv = 1000
        # Available 0
        self.assertEqual(obj.available_to_receive(), 0)
        # Error when item has been completely received and more is requested
        self.assertEqual(obj.receive_yarn(10), "Quantity issued on LC have already been received.")
        # Error when more quantity requested with edit receive method
        self.assertEqual(obj.edit_receive(100, 200), "Amount to receive cannot be more than amount available.")
        # Amount match to 950 when edit receive used to decrease quantity
        obj.yarn_rcv = 1000
        obj.edit_receive(100, 50)
        self.assertEqual(obj.yarn_rcv, 950)
        # Error when yarn delivery amount is more than yarn balance
        obj.yarn_rcv = 1000
        obj.yarn_bal = 0
        obj.yarn_dlv = 1000
        self.assertEqual(obj.deliver_yarn(100), "Amount to deliver is greater than current yarn balance.")
        # Same error when trying to edit yarn delivery to change to a greater amount
        self.assertEqual(obj.edit_deliver(50, 100), "Amount to deliver is greater than current yarn balance.")


class YarnRcvTests(TestCase):

    def setUp(self):
        lc = LC.objects.create(date="2017-12-08", number="0987654321", spinning_mill="Demo Spinning Mill")
        lc_item = LCItem.objects.create(
            lc=lc,
            count='unique',
            composition='100% Cotton',
            quantity=1000,
            unit='kg',
            style_no='Demo Style',
            color='Demo Color',
        )
        yr = YarnRcv.objects.create(
            lc_item = lc_item,
            date = "2017-12-08",
            challan_no = "67345",
            lot = "9823",
            quantity_rcv = 100
        )

    def test_yarn_receive(self):
        # See if YR item creation changes value in lc_item
        lc_item = LCItem.objects.get(count='unique')
        yr = YarnRcv.objects.get(lc_item=lc_item)
        self.assertEqual(yr.quantity_rcv, lc_item.yarn_rcv)
        # See if when YR is changed if lc_item is changed IMPORTANT # # # # ## # # # # # #
        yr.__setattr__('quantity_rcv', 200)
        yr.save()
        self.assertEqual(yr.quantity_rcv, lc_item.yarn_rcv)
