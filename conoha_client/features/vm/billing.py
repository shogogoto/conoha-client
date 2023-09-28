"""請求情報照会."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic.dataclasses import dataclass

from conoha_client.features._shared import Endpoints, utc2jst


@dataclass(frozen=True)
class VPSOrder:
    """VPS請求情報."""

    order_id: UUID
    product_name: str
    service_name: str
    billing_at: datetime
    unit_price: int
    status: str

    @classmethod
    def parse(cls, one: dict) -> VPSOrder:
        """HTTPレスポンスから請求情報へ変換.

        :param one: json["order_items"]: list[dict]の要素
        """
        return VPSOrder(
            order_id=UUID(one["uu_id"]),
            product_name=one["product_name"],
            service_name=one["service_name"],
            billing_at=utc2jst(one["bill_start_date"]),
            unit_price=one["unit_price"],
            status=one["status"],
        )


def detail_order(order_id: str) -> VPSOrder:
    """請求情報詳細を取得する."""
    res = Endpoints.ACCOUNT.get(f"order-items/{order_id}").json()
    return VPSOrder.parse(res["order_item"])


def payment_history() -> dict:
    """入金履歴.

    :return: [{
        "deposit_amount",
        "money_type",
        "received_data"}]
    """
    return Endpoints.ACCOUNT.get("payment-history").json()["payment_history"]


def payment_total() -> dict:
    """入金額合計.

    :return: {"total_deposit_amount"}
    """
    return Endpoints.ACCOUNT.get("payment-summary").json()["payment_summary"]


def billing_invoices(offset: int | None = 0, limit: int | None = 1000) -> dict:
    r"""課金一覧.

    https://www.conoha.jp/docs/account-billing-invoices-list.php
    :param offset: 取得開始位置
    :param limit: 取得数
    :return: [{
          "bill_plus_tax"\: 0,
          "due_date"\: "2023-04-30T15\:00\:00Z",
          "invoice_date"\: "2023-04-30T15\:00\:00Z",
          "invoice_id"\: 1359752607,
          "payment_method_type"\: "Charge"}]
    """
    params = {
        "offset": offset,
        "limit": limit,
    }
    return Endpoints.ACCOUNT.get("billing-invoices", params).json()["billing_invoices"]


def detail_invoice(invoice_id: str) -> dict:
    """課金詳細.

    :return: {
         'bill_plus_tax': 0,
         'due_date': '2023-04-30T15:00:00Z',
         'invoice_date': '2023-04-30T15:00:00Z',
         'invoice_id': 1359752607,
         'items': [{'end_date': '2023-04-30T14:59:59Z',
                    'invoice_detail_id': 433591413,
                    'product_name': 'VPSService SSD 30GB Memory 512M CPU 1Core',
                    'quantity': 720,
                    'start_date': '2023-03-31T15:00:00Z',
                    'unit_price': 1},
                   {'end_date': None,
                    'invoice_detail_id': 433591415,
                    'product_name': 'VPS割引きっぷ(100.00%)',
                    'quantity': 1,
                    'start_date': None,
                    'unit_price': 1}],
         'payment_method_type': 'Charge'}
    """
    return Endpoints.ACCOUNT.get(f"billing-invoices/{invoice_id}").json()[
        "billing_invoice"
    ]