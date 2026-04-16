#api_service/app/dataAccess/mock_impl.py

from api_service.app.dataAccess.base import DataResault, DataAccessor, MetadataResult, MetadataAccessor
from database.session import get_session
from sqlalchemy import text

class MockDataAccessor(DataAccessor):
    def fetch(self, request, payload: dict) -> DataResault:

        with get_session() as session:

            symbolname = payload["symbol"]
            normalized_symbol = symbolname.replace("-", "/")

            exchange = session.execute(
                text(
                    """select * from exchanges where name = :exchange """
                ), payload
            ).mappings().all()
            exchange_id = exchange[0]['id'] if exchange else None

            if not exchange_id:
                return DataResault(available=False, message='exchange not find', payload=[])

            symbol = session.execute(
                text(
                    """select * from canonical_symbols where symbol = :symbol limit 1"""
                ),{"symbol": normalized_symbol}
            ).mappings().all()
            symbol_id = symbol[0]['id'] if symbol else None


            exchange_market = session.execute(
                text(
                    """select * from exchange_markets 
                    where exchange_id = :ex_id and canonical_symbol_id = :sym_id and market_type = :market_type"""
                ), {"ex_id": exchange_id, 
                    "sym_id" : symbol_id, 
                    "market_type" : payload["market"].lower()
                    }
            ).mappings().all()
            exchange_market_id = exchange_market[0]['id'] if exchange_market else None
            
            if not exchange_market_id:
                return DataResault(available=False, message='exchange_market not find', payload=[])


            interval = session.execute(
                text(
                    """select * from intervals where interval = :interval """
                ),payload
            ).mappings().all()
            Interval_id = interval[0]['id'] if interval else None

            if not Interval_id:
                return DataResault(available=False, message='Interval not find', payload=[])

            rows = session.execute(
                text("""
                    select * from candles 
                     where exchange_market_id = :ex_market_id and 
                     interval_id = :interval  
                     limit 5
                """), {"ex_market_id": exchange_market_id, "interval": Interval_id}
            ).mappings().all()

        return DataResault(
            available=bool(rows),
            message='success',
            payload=rows
        )


class MockMetaDataAccessor(MetadataAccessor):
    def fetch(self, request, payload) -> MetadataResult:

        with get_session() as session:

            base_query = """
                    select 
                        e.name as exchange, 
                        REPLACE(cs.symbol, '/', '-') AS symbol, 
                        em.exchange_symbol, 
                        i.interval, 
                        em.market_type, 
                        s.status
                    from supported_markets s
                    join intervals i on s.interval_id = i.id 
                    join exchange_markets em on s.exchange_market_id = em.id
                    join exchanges e on em.exchange_id = e.id
                    join canonical_symbols cs on em.canonical_symbol_id = cs.id
                    where 1 = 1
                    """

            params = {}

            if payload.get("exchange"):
                base_query += " and e.name = :exchange"
                params["exchange"] = payload["exchange"]

            if payload.get("market"):
                base_query += " and em.market_type = :market"
                params["market"] = payload["market"]

            if payload.get("symbol"):
                base_query += " and REPLACE(cs.symbol, '/', '-') = :symbol"
                params["symbol"] = payload["symbol"]   

            if payload.get("interval"):
                base_query += " and i.interval = :interval"
                params["interval"] = payload["interval"]

            rows = session.execute(text(base_query),params).mappings().all()


            exchanges = {}

            for row in rows:
                ex = row['exchange']
                symbol = row["symbol"]
                market_type = row["market_type"]


                if ex not in exchanges:
                    exchanges[ex] = {}

                key = (symbol, market_type)

                if key not in exchanges[ex]:
                    exchanges[ex][key] = {
                        "symbol" : symbol,
                        "exchange_symbol" : row["exchange_symbol"],
                        "market_type" : market_type,
                        "intervals" : set() 
                    }
                exchanges[ex][key]["intervals"].add(row["interval"])


            result = {"exchanges": []}

            for ex_name, markets in exchanges.items():
                exchange_obj = {
                    "name": ex_name,
                    "markets": []
                }

                for market in markets.values():  # 👈 کلید tuple دیگه استفاده نمیشه
                    exchange_obj["markets"].append({
                        "symbol": market["symbol"],
                        "exchange_symbol": market["exchange_symbol"],
                        "market_type": market["market_type"],
                        "intervals": sorted(list(market["intervals"]))
                    })

                result["exchanges"].append(exchange_obj)

        return MetadataResult(available = bool(rows), payload = result)