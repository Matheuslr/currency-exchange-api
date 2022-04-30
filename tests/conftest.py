import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from mongomock import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.application import get_app
from app.settings import settings


@pytest.fixture(scope="session")
def currency_payload():
    return {"name": "real", "iso_4217": "BRL"}


@pytest.fixture(scope="session")
def currencies_payload():
    return [{"name": "real", "iso_4217": "BRL"}, {"name": "dolar", "iso_4217": "USD"}]


@pytest.fixture(scope="session")
def client():
    with (TestClient(get_app())) as client:
        yield client


# @pytest_asyncio.fixture()
# async def async_client(
#     app: FastAPI,
#     db_session: AsyncIOMotorClient,
# ) :
#     async def before_request(_):
#         await db_session.commit()
#         db_session.expire_all()

#     async with AsyncIOMotorClient(settings.mongo_url(),
#                 maxPoolSize=10,
#                 minPoolSize=10,) as ac:
#         yield ac


# class PyMongoMock(MongoClient):
#     def init_app(self, app):
#         return super().__init__()


@pytest.fixture
def exchangerate_api_response() -> dict:
    return {
        "motd": {
            "msg": "If you or your company use this project or like what we doing, please consider backing us so we can continue maintaining and evolving this project.",
            "url": "https://exchangerate.host/#/donate",
        },
        "success": True,
        "base": "BRL",
        "date": "2022-04-29",
        "rates": {
            "AED": 0.743738,
            "AFN": 17.308736,
            "ALL": 23.323969,
            "AMD": 93.170023,
            "ANG": 0.364274,
            "AOA": 82.539035,
            "ARS": 23.318631,
            "AUD": 0.282747,
            "AWG": 0.364572,
            "AZN": 0.344268,
            "BAM": 0.376636,
            "BBD": 0.404865,
            "BDT": 17.477158,
            "BGN": 0.376701,
            "BHD": 0.076479,
            "BIF": 415.061186,
            "BMD": 0.202594,
            "BND": 0.280483,
            "BOB": 1.389604,
            "BRL": 1,
            "BSD": 0.202572,
            "BTC": 0.000005,
            "BTN": 15.453686,
            "BWP": 2.454425,
            "BYN": 0.679955,
            "BZD": 0.407435,
            "CAD": 0.258247,
            "CDF": 405.667366,
            "CHF": 0.196516,
            "CLF": 0.006502,
            "CLP": 173.77129,
            "CNH": 1.343899,
            "CNY": 1.339592,
            "COP": 798.458035,
            "CRC": 133.707456,
            "CUC": 0.202609,
            "CUP": 5.21308,
            "CVE": 21.33718,
            "CZK": 4.723257,
            "DJF": 35.980529,
            "DKK": 1.43099,
            "DOP": 11.127819,
            "DZD": 29.2908,
            "EGP": 3.74279,
            "ERN": 3.03658,
            "ETB": 10.479024,
            "EUR": 0.192385,
            "FJD": 0.436693,
            "FKP": 0.162079,
            "GBP": 0.162031,
            "GEL": 0.617527,
            "GGP": 0.162065,
            "GHS": 1.520963,
            "GIP": 0.162064,
            "GMD": 10.901539,
            "GNF": 1794.599486,
            "GTQ": 1.54812,
            "GYD": 42.283164,
            "HKD": 1.588702,
            "HNL": 4.960718,
            "HRK": 1.456289,
            "HTG": 21.627786,
            "HUF": 72.751281,
            "IDR": 2922.71806,
            "ILS": 0.669889,
            "IMP": 0.162081,
            "INR": 15.485319,
            "IQD": 294.974207,
            "IRR": 8563.194835,
            "ISK": 26.49951,
            "JEP": 0.162029,
            "JMD": 31.256666,
            "JOD": 0.143535,
            "JPY": 26.403221,
            "KES": 23.394001,
            "KGS": 17.222469,
            "KHR": 817.321456,
            "KMF": 94.918826,
            "KPW": 182.195801,
            "KRW": 255.096963,
            "KWD": 0.062158,
            "KYD": 0.168645,
            "KZT": 90.31034,
            "LAK": 2433.34547,
            "LBP": 305.634333,
            "LKR": 70.737894,
            "LRD": 30.760833,
            "LSL": 3.234881,
            "LYD": 0.962928,
            "MAD": 2.020135,
            "MDL": 3.753318,
            "MGA": 816.503427,
            "MKD": 11.862307,
            "MMK": 374.198313,
            "MNT": 610.195766,
            "MOP": 1.633506,
            "MRU": 7.382133,
            "MUR": 8.705145,
            "MVR": 3.127821,
            "MWK": 165.04778,
            "MXN": 4.122965,
            "MYR": 0.881868,
            "MZN": 12.925887,
            "NAD": 3.241022,
            "NGN": 83.975419,
            "NIO": 7.238333,
            "NOK": 1.893995,
            "NPR": 24.725705,
            "NZD": 0.310383,
            "OMR": 0.077909,
            "PAB": 0.202667,
            "PEN": 0.773762,
            "PGK": 0.7125,
            "PHP": 10.585735,
            "PKR": 37.541315,
            "PLN": 0.900228,
            "PYG": 1382.333691,
            "QAR": 0.7372,
            "RON": 0.951707,
            "RSD": 22.61594,
            "RUB": 14.690141,
            "RWF": 205.865234,
            "SAR": 0.75936,
            "SBD": 1.625449,
            "SCR": 2.618944,
            "SDG": 90.49063,
            "SEK": 1.98844,
            "SGD": 0.279948,
            "SHP": 0.161987,
            "SLL": 2488.316614,
            "SOS": 116.917519,
            "SRD": 4.202049,
            "SSP": 26.369814,
            "STD": 4389.941208,
            "STN": 4.686622,
            "SVC": 1.768509,
            "SYP": 508.619423,
            "SZL": 3.220085,
            "THB": 6.949011,
            "TJS": 2.517221,
            "TMT": 0.710736,
            "TND": 0.620955,
            "TOP": 0.467009,
            "TRY": 2.99471,
            "TTD": 1.371825,
            "TWD": 5.95418,
            "TZS": 470.469618,
            "UAH": 6.113766,
            "UGX": 717.679547,
            "USD": 0.202583,
            "UYU": 8.394379,
            "UZS": 2268.504456,
            "VES": 0.903268,
            "VND": 4648.924138,
            "VUV": 22.739309,
            "WST": 0.522203,
            "XAF": 126.146312,
            "XAG": 0.008728,
            "XAU": 0.000271,
            "XCD": 0.547183,
            "XDR": 0.147461,
            "XOF": 126.146303,
            "XPD": 0.000118,
            "XPF": 22.948619,
            "XPT": 0.000279,
            "YER": 50.660641,
            "ZAR": 3.215499,
            "ZMW": 3.442679,
            "ZWL": 65.185581,
        },
    }
