from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.session import Base


#-------------------------------------------------------------------------
#exchange Model
#------------------------------------------------------------------------
class Exchange(Base):
    __tablename__ = "exchanges"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    status = Column(String, default="active")

    # relationships
    markets = relationship("ExchangeMarket", back_populates="exchange")
#------------------------------------------------------------------------


#-----------------------------------------------------------------------
# Canoncial Symbols Model
# ------------------------------------------------------------------------
class CanonicalSymbol(Base):
    __tablename__ = "canonical_symbols"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True, nullable=False)
    base_asset = Column(String, nullable=False)
    quote_asset = Column(String, nullable=False)

    # relationships
    markets = relationship("ExchangeMarket", back_populates="canonical_symbol")   
#-------------------------------------------------------------------------------


#-----------------------------------------------------------------
# Interval Model
#------------------------------------------------------------------
class Interval(Base):
    __tablename__ = "intervals"
    
    id = Column(Integer, primary_key=True)
    interval = Column(String, unique=True, nullable=False)
    ms = Column(Integer, nullable=False)

    # relationships
    supported_markets = relationship("SupportedMarket", back_populates="interval")
#---------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# ExchangeMarket Model
#--------------------------------------------------------------------------------
class ExchangeMarket(Base):
    __tablename__ = "exchange_markets"

    id = Column(Integer, primary_key=True)

    exchange_id = Column(Integer, ForeignKey("exchanges.id"), nullable=False)
    canonical_symbol_id = Column(Integer, ForeignKey("canonical_symbols.id"), nullable=False)

    exchange_symbol = Column(String, nullable=False)
    market_type = Column(String, nullable=False)

    # relationships
    exchange = relationship("Exchange", back_populates = "markets")
    canonical_symbol = relationship("CanonicalSymbol", back_populates= "markets")

    supported_markets = relationship("SupportedMarket", back_populates="exchange_market")
#---------------------------------------------------------------------------------------


#---------------------------------------------------------
# SupportedMarket Model
#---------------------------------------------------------
class SupportedMarket(Base):
    __tablename__ = "supported_markets"

    id = Column(Integer, primary_key=True)

    exchange_market_id = Column(Integer, ForeignKey("exchange_markets.id"), nullable=False)
    interval_id = Column(Integer, ForeignKey("intervals.id"), nullable=False)

    status = Column(String, default="active")

    # relationships
    exchange_market = relationship("ExchangeMarket", back_populates="supported_markets")
    interval = relationship("Interval", back_populates="supported_markets")
#--------------------------------------------------------------

