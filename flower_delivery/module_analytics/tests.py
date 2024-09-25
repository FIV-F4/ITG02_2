"""
Путь: module_analytics/tests.py
Тесты для приложения module_analytics.
"""
from django.test import TestCase
from module_analytics.models import Report, AggregateReport
from module_orders.models import Order
from module_catalog.models import Products
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

class ReportModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Products.objects.create(name='Роза', price=50.00, image='images/products/rose.jpg')
        self.order = Order.objects.create(user=self.user, status='ordered')
        self.report = Report.objects.create(
            order=self.order,
            sales_data=100.00,
            profit=50.00,
            expenses=20.00
        )

    def test_report_creation(self):
        """Проверка создания отчета и корректного представления"""
        self.assertEqual(self.report.sales_data, 100.00)
        self.assertEqual(self.report.profit, 50.00)
        self.assertEqual(self.report.expenses, 20.00)
        self.assertEqual(str(self.report), f"Отчет {self.report.id} по заказу {self.order.id} от {self.report.date}")

class AggregateReportModelTest(TestCase):
    def setUp(self):
        self.aggregate_report = AggregateReport.objects.create(
            period_type='daily',
            start_date=date.today(),
            end_date=date.today(),
            total_sales=1000.00,
            total_profit=500.00,
            total_expenses=200.00,
            total_orders=10,
            total_products_sold=30
        )

    def test_aggregate_report_creation(self):
        """Проверка создания агрегированного отчета и корректного представления"""
        self.assertEqual(self.aggregate_report.total_sales, 1000.00)
        self.assertEqual(self.aggregate_report.total_profit, 500.00)
        self.assertEqual(self.aggregate_report.total_expenses, 200.00)
        self.assertEqual(self.aggregate_report.total_orders, 10)
        self.assertEqual(self.aggregate_report.total_products_sold, 30)
        self.assertEqual(
            str(self.aggregate_report),
            f"{self.aggregate_report.get_period_type_display()} отчет с {self.aggregate_report.start_date} по {self.aggregate_report.end_date}"
        )

