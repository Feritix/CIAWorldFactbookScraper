import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
import re

def quantity(value):
    value = re.sub(r'\(.+\)', '', value)
    multiplier = 1
    if 'million' in value:
        multiplier = 10**6
    elif 'billion' in value:
        multiplier = 10**9
    elif 'trillion' in value:
        multiplier = 10**12
    value = re.search(r'(-?\d{1,3}(,\d{3})*\.?\d*)', value)
    if value:
        value = value.group().replace(',', '')
        value = float(value) * multiplier
        return round(value, 2)
    else:
        return None

def percentage(value):
    value = re.sub(r'\(.+\)', '', value)
    value = re.search(r'-?\d{1,2}\.?\d*(?=%)', value)
    if value:
        return float(value.group())
    else:
        return None
    

class WfbCiaItem(scrapy.Item):
    raw_string = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    quantity_item = scrapy.Field(input_processor = MapCompose(remove_tags, quantity), output_processor = TakeFirst())
    percentage_item = scrapy.Field(input_processor = MapCompose(remove_tags, percentage), output_processor = TakeFirst())

    country = raw_string
    
    area_total_sq_km = quantity_item
    area_land_sq_km = quantity_item
    area_water_sq_km = quantity_item
    
    highest_point_m = quantity_item
    raw_highest_point_m = raw_string
    lowest_point_m = quantity_item
    mean_elevation_m = quantity_item

    agricultural_land_per = percentage_item
    arable_land_per = percentage_item
    permanent_crops_per = percentage_item
    permanent_pasture_per = percentage_item
    forest_land_per = percentage_item
    other_land_per = percentage_item

    irrigated_land_sq_km = quantity_item

    population = quantity_item

    age_per_0_14 = percentage_item
    age_pop_15_24 = percentage_item
    age_pop_25_54 = percentage_item
    age_pop_55_64 = percentage_item
    age_pop_65_plus = percentage_item

    total_dependency_ratio = quantity_item
    youth_dependency_ratio = quantity_item
    elderly_dependency_ratio = quantity_item
    potential_support_ratio = quantity_item

    median_age_total = quantity_item
    median_age_male = quantity_item
    median_age_female = quantity_item

    population_growth_rate = percentage_item

    birth_rate_per_1k = quantity_item

    death_rate_per_1k = quantity_item

    net_migration_rate_per_1k = quantity_item

    urban_population_per = percentage_item
    annual_urbanization_rate_per = percentage_item

    sex_ratio_mtf_birth = quantity_item
    sex_ratio_mtf_0_14 = quantity_item
    sex_ratio_mtf_15_24 = quantity_item
    sex_ratio_mtf_25_54 = quantity_item
    sex_ratio_mtf_55_64 = quantity_item
    sex_ratio_mtf_65_plus = quantity_item
    sex_ratio_mtf_total = quantity_item

    mother_mean_age_first_birth = quantity_item

    maternal_mortality_per_100k = quantity_item

    infant_mortality_per_1k_total = quantity_item
    infant_mortality_per_1k_male = quantity_item
    infant_mortality_per_1k_female = quantity_item

    life_expectancy_total = quantity_item
    life_expectancy_male = quantity_item
    life_expectancy_female = quantity_item

    fertility_child_per_woman = quantity_item

    contraceptive_rate_per = percentage_item

    drinking_water_improved_urban_per = percentage_item
    drinking_water_improved_rural_per = percentage_item
    drinking_water_improved_total_per = percentage_item
    drinking_water_unimproved_urban_per = percentage_item
    drinking_water_unimproved_rural_per = percentage_item
    drinking_water_unimproved_total_per = percentage_item

    health_expenditure_per_gdp = percentage_item

    physician_density_per_1k = quantity_item

    hospital_beds_per_1k = quantity_item

    sanitation_access_improved_urban_per = percentage_item
    sanitation_access_improved_rural_per = percentage_item
    sanitation_access_improved_total_per = percentage_item
    sanitation_access_unimproved_urban_per = percentage_item
    sanitation_access_unimproved_rural_per = percentage_item
    sanitation_access_unimproved_total_per = percentage_item

    hiv_aids_prevalence_per = percentage_item

    hiv_aids_prevalence_total = quantity_item
    
    hiv_aids_deaths = quantity_item

    obesity_per = percentage_item

    alcohol_per_capita_total_l = quantity_item
    alcohol_per_capita_beer_l = quantity_item
    alcohol_per_capita_wine_l = quantity_item
    alcohol_per_capita_spirits_l = quantity_item
    alcohol_per_capita_other_l = quantity_item

    tobacco_use_per_total = percentage_item
    tobacco_use_per_male = percentage_item
    tobacco_use_per_female = percentage_item

    children_under_5_underweight_per = percentage_item

    education_expenditures_per_gdp = percentage_item

    literacy_over_15yrs_per_total = percentage_item
    literacy_over_15yrs_per_male = percentage_item
    literacy_over_15yrs_per_female = percentage_item

    school_life_expectancy_yrs_total = quantity_item
    school_life_expectancy_yrs_male = quantity_item
    school_life_expectancy_yrs_female = quantity_item

    unemployment_ages_15_24_per_total = percentage_item
    unemployment_ages_15_24_per_male = percentage_item
    unemployment_ages_15_24_per_female = percentage_item

    particulate_emissions_ug_per_meter3 = quantity_item ####
    co2_emissions_megatons = quantity_item
    methane_emissions_megatons = quantity_item

    revenue_from_forests_per_gdp = percentage_item
    
    revenue_from_coal_per_gdp = percentage_item

    annual_waste_generated_tons = quantity_item
    annual_waste_recycled_tons = quantity_item
    recycled_waste_per = percentage_item

    water_withdrawal_muni_meter3 = quantity_item
    water_withdrawal_indust_meter3 = quantity_item
    water_withdrawal_ag_meter3 = quantity_item

    total_renewable_water_meter3 = quantity_item

    government_type = raw_string

    real_gdp_ppp = quantity_item ###

    real_gdp_growth_per = percentage_item

    gdp_per_capita = quantity_item

    gdp_oer = quantity_item

    inflation_rate = percentage_item

    s_and_p_credit_rating = raw_string

    gdp_comp_sector_agriculture_per = percentage_item
    gdp_comp_sector_industry_per = percentage_item
    gdp_comp_sector_services_per = percentage_item

    gdp_comp_end_use_household_per = percentage_item
    gdp_comp_end_use_gov_per = percentage_item
    gdp_comp_end_use_fixed_cap_investment_per = percentage_item
    gdp_comp_end_use_inventory_investment__per = percentage_item
    gdp_comp_end_use_exports_per = percentage_item
    gdp_comp_end_use_imports_per = percentage_item

    industrial_prod_growth_rate = percentage_item

    labor_force_total = quantity_item

    labor_force_occupation_agriculture_per = percentage_item
    labor_force_occupation_industry_per = percentage_item
    labor_force_occupation_services_per = percentage_item
    labor_force_occupation_industry_and_services_per = percentage_item
    labor_force_occupation_manufacturing_per = percentage_item
    labor_force_occupation_farm_forest_fish_per = percentage_item
    labor_force_occupation_manufacture_extract_trans_crafts_per = percentage_item
    labor_force_occupation_managerial_technical_per = percentage_item
    labor_force_occupation_sale_office_per = percentage_item
    labor_force_occupation_other_per = percentage_item

    unemployment_rate_total = percentage_item

    pop_below_poverty_line = percentage_item

    gini_coefficient = quantity_item

    income_or_consumption_per_lowest_10per = percentage_item
    income_or_consumption_per_highest_10per = percentage_item

    budget_revenues = quantity_item
    budget_expenditures = quantity_item

    budget_surplus_or_deficit = percentage_item

    public_debt_per_gdp = percentage_item

    taxes_per_of_gdp = percentage_item

    account_balance = quantity_item

    exports_dollars = quantity_item

    imports_dollars = quantity_item

    reserves_forex_and_gold = quantity_item

    external_debt = quantity_item

    electricity_access_total_per = percentage_item
    electricity_access_urban_per = percentage_item
    electricity_access_rural_per = percentage_item

    electricity_generating_cap_kw = quantity_item
    electricity_consumption_kwh = quantity_item
    electricity_exports_kwh = quantity_item
    electricity_imports_kwh = quantity_item
    electricity_transmission_losses_kwh = quantity_item

    electricity_source_fossil_fuel_per = percentage_item
    electricity_source_nuclear_per = percentage_item
    electricity_source_solar_per = percentage_item
    electricity_source_wind_per = percentage_item
    electricity_source_hydroelectric_per = percentage_item
    electricity_source_tide_and_wave_per = percentage_item
    electricity_source_geothermal_per = percentage_item
    electricity_source_biomass_per = percentage_item

    coal_production_mton = quantity_item
    coal_consumption_mton = quantity_item
    coal_exports_mton = quantity_item
    coal_imports_mton = quantity_item
    coal_proven_reserves_mton = quantity_item

    petroleum_production_bbl_per_day = quantity_item
    petroleum_consumption_bbl_per_day = quantity_item
    petroleum_exports_bbl_per_day = quantity_item
    petroleum_imports_bbl_per_day = quantity_item
    petroleum_estimated_reserves_bbl = quantity_item

    refined_petroleum_production_bbl_per_day = quantity_item

    refined_petroleum_exports_bbl_per_day = quantity_item

    refined_petroleum_imports_bbl_per_day = quantity_item

    natural_gas_production_meter3 = quantity_item
    natural_gas_cunsuption_meter3 = quantity_item
    natural_gas_exports_meter3 = quantity_item
    natural_gas_imports_meter3 = quantity_item
    natural_gas_proven_reserves_meter3 = quantity_item

    co2_emissions_total_mtons = quantity_item
    co2_emissions_coal_and_coke_mtons = quantity_item
    co2_emissions_petroleum_mtons = quantity_item
    co2_emissions_natural_gas_mtons = quantity_item

    energy_consumption_per_capita_btu = quantity_item

    telephone_landline_subscriptions_total = quantity_item
    telephone_landline_subscriptions_per_100 = quantity_item

    mobile_phone_subscriptions_total = quantity_item
    mobile_phone_subscriptions_per_100 = quantity_item

    internet_users_total = quantity_item
    internet_users_per_pop = percentage_item

    fixed_broadband_subscriptions_total = quantity_item
    fixed_broadband_subscriptions_per_100 = quantity_item

    registered_airlines_quantity = quantity_item
    registered_airlines_number_of_aircraft = quantity_item
    annual_airline_passenger_traffic = quantity_item
    annual_airline_freight_traffic = quantity_item

    civil_aircraft_registration_code_prefix = raw_string

    airports_total = quantity_item

    airports_paved_total = quantity_item
    airports_paved_over_3047m = quantity_item
    airports_paved_2438_to_3047m = quantity_item
    airports_paved_1524_to_2437m = quantity_item
    airports_paved_914_to_1523m = quantity_item
    airports_paved_under_914m = quantity_item

    airports_unpaved_total = quantity_item
    airports_unpaved_over_3047m = quantity_item
    airports_unpaved_2438_to_3047m = quantity_item
    airports_unpaved_1524_to_2437m = quantity_item
    airports_unpaved_914_to_1523m = quantity_item
    airports_unpaved_under_914m = quantity_item

    heliports_total = quantity_item

    railways_total = quantity_item
    railways_standard_gauge = quantity_item
    railways_narrow_gauge = quantity_item
    railways_broad_gauge = quantity_item
    railways_dual_gauge = quantity_item

    roads_total_km = quantity_item
    roads_paved_km = quantity_item
    roads_unpaved_km = quantity_item
    roads_urban_km = quantity_item
    roads_non_urban_km = quantity_item

    waterways_km = quantity_item
    
    merchant_marine_watercraft_total = quantity_item

    military_expenditures_per_gdp = percentage_item

