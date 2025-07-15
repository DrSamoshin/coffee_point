import logging
import pandas as pd
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import order as crud_order
from app.db.db_sessions import get_point_db
from app.services.authentication import get_user_id_from_token

router = APIRouter(prefix="/orders-report", tags=["orders_report"])


@router.get("/{shift_id}/")
async def get_products_shift_orders_report(
    shift_id: UUID,
    db: Session = Depends(get_point_db),
    user_id: str = Depends(get_user_id_from_token),
):
    try:
        shift_orders_products = crud_order.get_products_for_shift_order(db, shift_id)
        df = pd.DataFrame(shift_orders_products)
        df["total_product_price"] = df["product_price"] * df["count"]

        # debit True order products
        df_debit_true_products = df[df["debit"] == True]
        debit_true_product_amount = len(df_debit_true_products)
        debit_true_products_sum = (
            df_debit_true_products.groupby("product_name")
            .agg(
                {
                    "product_category": "first",
                    "count": "sum",
                    "total_product_price": "sum",
                }
            )
            .sort_values(
                by=["product_category", "total_product_price"], ascending=[True, False]
            )
            .reset_index()
        )

        # unique orders
        df_debit_true_orders = df_debit_true_products[
            [
                "order_id",
                "order_date",
                "order_price",
                "order_discount",
                "order_payment_method",
                "order_type",
                "order_status",
                "product_category",
            ]
        ]
        df_debit_true_unique_orders = df_debit_true_orders.drop_duplicates(
            subset=["order_id"]
        )

        df_debit_true_category_product_for_order = (
            df_debit_true_products.groupby(
                ["order_id", "product_category", "order_date"]
            )
            .size()
            .reset_index(name="count")
        )

        debit_true_unique_order_amount = len(df_debit_true_unique_orders)
        income_debit_true_orders = df_debit_true_unique_orders["order_price"].sum()

        # debit False order products
        df_debit_false_products = df[df["debit"] == False]
        debit_false_product_amount = len(df_debit_false_products)
        debit_false_products_sum = (
            df_debit_false_products.groupby("product_name")
            .agg(
                {
                    "product_category": "first",
                    "count": "sum",
                    "total_product_price": "sum",
                }
            )
            .sort_values(
                by=["product_category", "total_product_price"], ascending=[True, False]
            )
            .reset_index()
        )

        # unique orders
        df_debit_false_orders = df_debit_false_products[
            [
                "order_id",
                "order_date",
                "order_price",
                "order_discount",
                "order_payment_method",
                "order_type",
                "order_status",
            ]
        ]
        df_debit_false_unique_orders = df_debit_false_orders.drop_duplicates(
            subset=["order_id"]
        )

        df_debit_false_category_product_for_order = (
            df_debit_false_products.groupby(
                ["order_id", "product_category", "order_date"]
            )
            .size()
            .reset_index(name="count")
        )

        debit_false_unique_order_amount = len(df_debit_false_unique_orders)
        income_debit_false_orders = df_debit_false_unique_orders["order_price"].sum()

        # final result
        total_income = income_debit_false_orders - income_debit_true_orders
        total_number_sold_products = (
            debit_false_product_amount - debit_true_product_amount
        )
        average_bill = total_income / (
            debit_false_unique_order_amount - debit_true_unique_order_amount
        )

        debit_true_products_sum_json = debit_true_products_sum.to_dict(orient="records")
        debit_false_products_sum_json = debit_false_products_sum.to_dict(
            orient="records"
        )

        debit_true_unique_orders_json = df_debit_true_unique_orders.to_dict(
            orient="records"
        )
        debit_false_unique_orders_json = df_debit_false_unique_orders.to_dict(
            orient="records"
        )

        df_debit_true_category_product_for_order_json = (
            df_debit_true_category_product_for_order.to_dict(orient="records")
        )
        df_debit_false_category_product_for_order_json = (
            df_debit_false_category_product_for_order.to_dict(orient="records")
        )

        final_result = {
            "total_income": total_income,
            "total_number_sold_products": total_number_sold_products,
            "total_number_orders": debit_false_unique_order_amount,
            "total_number_debited_orders": debit_true_unique_order_amount,
            "average_bill": average_bill,
            "debit_true_products_sum_json": debit_true_products_sum_json,
            "debit_false_products_sum_json": debit_false_products_sum_json,
            "debit_true_unique_orders_json": debit_true_unique_orders_json,
            "debit_false_unique_orders_json": debit_false_unique_orders_json,
            "df_debit_true_category_product_for_order_json": df_debit_true_category_product_for_order_json,
            "df_debit_false_category_product_for_order_json": df_debit_false_category_product_for_order_json,
        }
    except HTTPException as http_exc:
        logging.error(f"{http_exc}")
        raise http_exc
    else:
        return final_result
