import scrapy
import json
from wfb_cia.items import WfbCiaItem
from scrapy.loader import ItemLoader


class WfbDataSpider(scrapy.Spider):
    name = 'wfb_data'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'ROBOTSTXT_OBEY': False,
    }
    start_urls = ['https://www.cia.gov/the-world-factbook/page-data/countries/page-data.json']

    def parse(self, response):
        data = json.loads(response.text)
        for country in data['result']['data']['countries']['edges']:
            country_uri = country['node']['uri']
            country_url = 'https://www.cia.gov/the-world-factbook' + country_uri
            yield response.follow(
                country_url,
                callback=self.parse_country,
            )

    def parse_country(self, response):
        loader = ItemLoader(item=WfbCiaItem(), selector=response.css('div.site'))
        
        def strong_path(h3, strong):
            return f'//div[h3/a = "{h3}"]/p/strong[contains(text(), "{strong}")]/following-sibling::text()[1]'

        def text_path(h3, text):
            return f'//div[h3/a = "{h3}"]/p/text()[contains(., "{text}")]'

        def header_path(h3):
            return f'//div[h3/a = "{h3}"]/p/text()[1]'

        def strong_text_path(h3, strong, text):
            return f'//div[h3/a = "{h3}"]/p/strong[contains(text(), "{strong}")]/following-sibling::text()[contains(., "{text}")]'
        
        loader.add_xpath('country', '//h1[@class="hero-title"]/text()')
        
        loader.add_xpath('area_total_sq_km', strong_path('Area', 'total'))
        loader.add_xpath('area_land_sq_km', strong_path('Area', 'land'))
        loader.add_xpath('area_water_sq_km', strong_path('Area', 'water'))
        
        loader.add_xpath('highest_point_m', strong_path('Elevation', 'highest'))
        loader.add_xpath('raw_highest_point_m', strong_path('Elevation', 'highest'))
        loader.add_xpath('lowest_point_m', strong_path('Elevation', 'lowest'))
        loader.add_xpath('mean_elevation_m', strong_path('Elevation', 'mean'))

        loader.add_xpath('agricultural_land_per', strong_path('Land use', 'agricultural'))
        loader.add_xpath('arable_land_per', text_path('Land use', 'arable'))
        loader.add_xpath('permanent_crops_per', text_path('Land use', 'crops'))
        loader.add_xpath('permanent_pasture_per', text_path('Land use', 'pasture'))
        loader.add_xpath('forest_land_per', strong_path('Land use', 'forest'))
        loader.add_xpath('other_land_per', strong_path('Land use', 'other'))

        loader.add_xpath('irrigated_land_sq_km', header_path('Irrigated land'))

        loader.add_xpath('population', header_path('Population'))

        loader.add_xpath('age_per_0_14', strong_path('Age structure', '0-14'))
        loader.add_xpath('age_pop_15_24', strong_path('Age structure', '15-24'))
        loader.add_xpath('age_pop_25_54', strong_path('Age structure', '25-54'))
        loader.add_xpath('age_pop_55_64', strong_path('Age structure', '55-64'))
        loader.add_xpath('age_pop_65_plus', strong_path('Age structure', '65'))

        loader.add_xpath('total_dependency_ratio', strong_path('Dependency ratios', 'total'))
        loader.add_xpath('youth_dependency_ratio', strong_path('Dependency ratios', 'youth'))
        loader.add_xpath('elderly_dependency_ratio', strong_path('Dependency ratios', 'elderly'))
        loader.add_xpath('potential_support_ratio', strong_path('Dependency ratios', 'support'))

        loader.add_xpath('median_age_total', strong_path('Median age', 'total'))
        loader.add_xpath('median_age_male', strong_path('Median age', 'male'))
        loader.add_xpath('median_age_female', strong_path('Median age', 'female'))

        loader.add_xpath('population_growth_rate', header_path('Population growth rate'))

        loader.add_xpath('birth_rate_per_1k', header_path('Birth rate'))

        loader.add_xpath('death_rate_per_1k', header_path('Death rate'))

        loader.add_xpath('net_migration_rate_per_1k', header_path('Net migration rate'))

        loader.add_xpath('urban_population_per', strong_path('Urbanization', 'population'))
        loader.add_xpath('annual_urbanization_rate_per', strong_path('Urbanization', 'rate'))

        loader.add_xpath('sex_ratio_mtf_birth', strong_path('Sex ratio', 'birth'))
        loader.add_xpath('sex_ratio_mtf_0_14', strong_path('Sex ratio', '0-14'))
        loader.add_xpath('sex_ratio_mtf_15_24', strong_path('Sex ratio', '15-24'))
        loader.add_xpath('sex_ratio_mtf_25_54', strong_path('Sex ratio', '25-54'))
        loader.add_xpath('sex_ratio_mtf_55_64', strong_path('Sex ratio', '55-64'))
        loader.add_xpath('sex_ratio_mtf_65_plus', strong_path('Sex ratio', '65'))
        loader.add_xpath('sex_ratio_mtf_total', strong_path('Sex ratio', 'total'))

        loader.add_xpath('mother_mean_age_first_birth', header_path('Mother\'s mean age at first birth'))

        loader.add_xpath('maternal_mortality_per_100k', header_path('Maternal mortality ratio'))

        loader.add_xpath('infant_mortality_per_1k_total', strong_path('Infant mortality rate', 'total'))
        loader.add_xpath('infant_mortality_per_1k_male', strong_path('Infant mortality rate', 'male'))
        loader.add_xpath('infant_mortality_per_1k_female', strong_path('Infant mortality rate', 'female'))

        loader.add_xpath('life_expectancy_total', strong_path('Life expectancy at birth', 'total'))
        loader.add_xpath('life_expectancy_male', strong_path('Life expectancy at birth', 'male'))
        loader.add_xpath('life_expectancy_female', strong_path('Life expectancy at birth', 'female'))

        loader.add_xpath('fertility_child_per_woman', header_path('Total fertility rate'))

        loader.add_xpath('contraceptive_rate_per', header_path('Contraceptive prevalence rate'))

        loader.add_xpath('drinking_water_improved_urban_per', strong_text_path('Drinking water source', 'improved', 'urban'))
        loader.add_xpath('drinking_water_improved_rural_per', strong_text_path('Drinking water source', 'improved', 'rural'))
        loader.add_xpath('drinking_water_improved_total_per', strong_text_path('Drinking water source', 'improved', 'total'))
        loader.add_xpath('drinking_water_unimproved_urban_per', strong_text_path('Drinking water source', 'unimproved', 'urban'))
        loader.add_xpath('drinking_water_unimproved_rural_per', strong_text_path('Drinking water source', 'unimproved', 'rural'))
        loader.add_xpath('drinking_water_unimproved_total_per', strong_text_path('Drinking water source', 'unimproved', 'total'))

        loader.add_xpath('health_expenditure_per_gdp', header_path('Current health expenditure'))

        loader.add_xpath('physician_density_per_1k', header_path('Physicians density'))

        loader.add_xpath('hospital_beds_per_1k', header_path('Hospital bed density'))

        loader.add_xpath('sanitation_access_improved_urban_per', strong_text_path('Sanitation facility access', 'improved', 'urban'))
        loader.add_xpath('sanitation_access_improved_rural_per', strong_text_path('Sanitation facility access', 'improved', 'rural'))
        loader.add_xpath('sanitation_access_improved_total_per', strong_text_path('Sanitation facility access', 'improved', 'total'))
        loader.add_xpath('sanitation_access_unimproved_urban_per', strong_text_path('Sanitation facility access', 'unimproved', 'urban'))
        loader.add_xpath('sanitation_access_unimproved_rural_per', strong_text_path('Sanitation facility access', 'unimproved', 'rural'))
        loader.add_xpath('sanitation_access_unimproved_total_per', strong_text_path('Sanitation facility access', 'unimproved', 'total'))

        loader.add_xpath('hiv_aids_prevalence_per', header_path('HIV/AIDS - adult prevalence rate'))

        loader.add_xpath('hiv_aids_prevalence_total', header_path('HIV/AIDS - people living with HIV/AIDS'))

        loader.add_xpath('hiv_aids_deaths', header_path('HIV/AIDS - deaths'))

        loader.add_xpath('obesity_per', header_path('Obesity - adult prevalence rate'))

        loader.add_xpath('alcohol_per_capita_total_l', strong_path('Alcohol consumption per capita', 'total'))
        loader.add_xpath('alcohol_per_capita_beer_l', strong_path('Alcohol consumption per capita', 'beer'))
        loader.add_xpath('alcohol_per_capita_wine_l', strong_path('Alcohol consumption per capita', 'wine'))
        loader.add_xpath('alcohol_per_capita_spirits_l', strong_path('Alcohol consumption per capita', 'spirits'))
        loader.add_xpath('alcohol_per_capita_other_l', strong_path('Alcohol consumption per capita', 'other'))

        loader.add_xpath('tobacco_use_per_total', strong_path('Tobacco use', 'total'))
        loader.add_xpath('tobacco_use_per_male', strong_path('Tobacco use', 'male'))
        loader.add_xpath('tobacco_use_per_female', strong_path('Tobacco use', 'female'))

        loader.add_xpath('children_under_5_underweight_per', header_path('Children under the age of 5 years underweight'))

        loader.add_xpath('education_expenditures_per_gdp', header_path('Education expenditures'))

        loader.add_xpath('literacy_over_15yrs_per_total', strong_path('Literacy', 'total'))
        loader.add_xpath('literacy_over_15yrs_per_male', strong_path('Literacy', 'male'))
        loader.add_xpath('literacy_over_15yrs_per_female', strong_path('Literacy', 'female'))

        loader.add_xpath('school_life_expectancy_yrs_total', strong_path('School life expectancy (primary to tertiary education)', 'total'))
        loader.add_xpath('school_life_expectancy_yrs_male', strong_path('School life expectancy (primary to tertiary education)', 'male'))
        loader.add_xpath('school_life_expectancy_yrs_female', strong_path('School life expectancy (primary to tertiary education)', 'female'))

        loader.add_xpath('unemployment_ages_15_24_per_total', strong_path('Unemployment, youth ages 15-24', 'total'))
        loader.add_xpath('unemployment_ages_15_24_per_male', strong_path('Unemployment, youth ages 15-24', 'male'))
        loader.add_xpath('unemployment_ages_15_24_per_female', strong_path('Unemployment, youth ages 15-24', 'female'))

        loader.add_xpath('particulate_emissions_ug_per_meter3', strong_path('Air pollutants', 'particulate'))
        loader.add_xpath('co2_emissions_megatons', strong_path('Air pollutants', 'carbon'))
        loader.add_xpath('methane_emissions_megatons', strong_path('Air pollutants', 'methane'))

        loader.add_xpath('revenue_from_forests_per_gdp', header_path('Revenue from forest resources'))

        loader.add_xpath('revenue_from_coal_per_gdp', header_path('Revenue from coal'))

        loader.add_xpath('annual_waste_generated_tons', strong_path('Waste and recycling', 'generated'))
        loader.add_xpath('annual_waste_recycled_tons', strong_path('Waste and recycling', 'recycled annually'))
        loader.add_xpath('recycled_waste_per', strong_path('Waste and recycling', 'percent'))

        loader.add_xpath('water_withdrawal_muni_meter3', strong_path('Total water withdrawal', 'municipal'))
        loader.add_xpath('water_withdrawal_indust_meter3', strong_path('Total water withdrawal', 'industrial'))
        loader.add_xpath('water_withdrawal_ag_meter3', strong_path('Total water withdrawal', 'agricultural'))

        loader.add_xpath('total_renewable_water_meter3', header_path('Total renewable water resources'))

        loader.add_xpath('government_type', header_path('Government type'))

        loader.add_xpath('real_gdp_ppp', header_path('Real GDP (purchasing power parity)'))
       
        loader.add_xpath('real_gdp_growth_per', header_path('Real GDP growth rate'))

        loader.add_xpath('gdp_per_capita', header_path('Real GDP per capita'))

        loader.add_xpath('gdp_oer', header_path('GDP (official exchange rate)'))

        loader.add_xpath('inflation_rate', header_path('Inflation rate (consumer prices)'))

        loader.add_xpath('s_and_p_credit_rating', strong_path('Credit ratings', 'Standard'))

        loader.add_xpath('gdp_comp_sector_agriculture_per', strong_path('GDP - composition, by sector of origin', 'agriculture'))
        loader.add_xpath('gdp_comp_sector_industry_per', strong_path('GDP - composition, by sector of origin', 'industry'))
        loader.add_xpath('gdp_comp_sector_services_per', strong_path('GDP - composition, by sector of origin', 'services'))

        loader.add_xpath('gdp_comp_end_use_household_per', strong_path('GDP - composition, by end use', 'household'))
        loader.add_xpath('gdp_comp_end_use_gov_per', strong_path('GDP - composition, by end use', 'government'))
        loader.add_xpath('gdp_comp_end_use_fixed_cap_investment_per', strong_path('GDP - composition, by end use', 'fixed'))
        loader.add_xpath('gdp_comp_end_use_inventory_investment__per', strong_path('GDP - composition, by end use', 'inventories'))
        loader.add_xpath('gdp_comp_end_use_exports_per', strong_path('GDP - composition, by end use', 'exports'))
        loader.add_xpath('gdp_comp_end_use_imports_per', strong_path('GDP - composition, by end use', 'imports'))

        loader.add_xpath('industrial_prod_growth_rate', header_path('Industrial production growth rate'))

        loader.add_xpath('labor_force_total', header_path('Labor force'))

        loader.add_xpath('labor_force_occupation_agriculture_per', strong_path('Labor force - by occupation', 'agriculture'))
        loader.add_xpath('labor_force_occupation_industry_per', strong_path('Labor force - by occupation', 'industry'))
        loader.add_xpath('labor_force_occupation_services_per', strong_path('Labor force - by occupation', 'services'))
        loader.add_xpath('labor_force_occupation_industry_and_services_per', strong_path('Labor force - by occupation', 'industry and services'))
        loader.add_xpath('labor_force_occupation_manufacturing_per', strong_path('Labor force - by occupation', 'manufacturing'))
        loader.add_xpath('labor_force_occupation_farm_forest_fish_per', strong_path('Labor force - by occupation', 'farming'))
        loader.add_xpath('labor_force_occupation_manufacture_extract_trans_crafts_per', strong_path('Labor force - by occupation', 'extraction'))
        loader.add_xpath('labor_force_occupation_managerial_technical_per', strong_path('Labor force - by occupation', 'managerial'))
        loader.add_xpath('labor_force_occupation_sale_office_per', strong_path('Labor force - by occupation', 'sales'))
        loader.add_xpath('labor_force_occupation_other_per', strong_path('Labor force - by occupation', 'other'))

        loader.add_xpath('unemployment_rate_total', header_path('Unemployment rate'))

        loader.add_xpath('pop_below_poverty_line', header_path('Population below poverty line'))

        loader.add_xpath('gini_coefficient', header_path('Gini Index coefficient - distribution of family income'))

        loader.add_xpath('income_or_consumption_per_lowest_10per', strong_path('Household income or consumption by percentage share', 'lowest'))
        loader.add_xpath('income_or_consumption_per_highest_10per', strong_path('Household income or consumption by percentage share', 'highest'))

        loader.add_xpath('budget_revenues', strong_path('Budget', 'revenues'))
        loader.add_xpath('budget_expenditures', strong_path('Budget', 'expenditures'))

        loader.add_xpath('budget_surplus_or_deficit', header_path('Budget surplus (+) or deficit (-)'))

        loader.add_xpath('public_debt_per_gdp', header_path('Public debt'))

        loader.add_xpath('taxes_per_of_gdp', header_path('Taxes and other revenues'))

        loader.add_xpath('account_balance', header_path('Current account balance'))

        loader.add_xpath('exports_dollars', header_path('Exports'))

        loader.add_xpath('imports_dollars', header_path('Imports'))

        loader.add_xpath('reserves_forex_and_gold', header_path('Reserves of foreign exchange and gold'))

        loader.add_xpath('external_debt', header_path('Debt - external'))

        loader.add_xpath('electricity_access_total_per', strong_path('Electricity access', 'total'))
        loader.add_xpath('electricity_access_urban_per', strong_path('Electricity access', 'urban'))
        loader.add_xpath('electricity_access_rural_per', strong_path('Electricity access', 'rural'))

        loader.add_xpath('electricity_generating_cap_kw', strong_path('Electricity', 'installed'))
        loader.add_xpath('electricity_consumption_kwh', strong_path('Electricity', 'consumption'))
        loader.add_xpath('electricity_exports_kwh', strong_path('Electricity', 'exports'))
        loader.add_xpath('electricity_imports_kwh', strong_path('Electricity', 'imports'))
        loader.add_xpath('electricity_transmission_losses_kwh', strong_path('Electricity', 'transmission'))

        loader.add_xpath('electricity_source_fossil_fuel_per', strong_path('Electricity generation sources', 'fossil'))
        loader.add_xpath('electricity_source_nuclear_per', strong_path('Electricity generation sources', 'nuclear'))
        loader.add_xpath('electricity_source_solar_per', strong_path('Electricity generation sources', 'solar'))
        loader.add_xpath('electricity_source_wind_per', strong_path('Electricity generation sources', 'wind'))
        loader.add_xpath('electricity_source_hydroelectric_per', strong_path('Electricity generation sources', 'hydroelectricity'))
        loader.add_xpath('electricity_source_tide_and_wave_per', strong_path('Electricity generation sources', 'tide'))
        loader.add_xpath('electricity_source_geothermal_per', strong_path('Electricity generation sources', 'geothermal'))
        loader.add_xpath('electricity_source_biomass_per', strong_path('Electricity generation sources', 'biomass'))

        loader.add_xpath('coal_production_mton', strong_path('Coal', 'production'))
        loader.add_xpath('coal_consumption_mton', strong_path('Coal', 'consumption'))
        loader.add_xpath('coal_exports_mton', strong_path('Coal', 'exports'))
        loader.add_xpath('coal_imports_mton', strong_path('Coal', 'imports'))
        loader.add_xpath('coal_proven_reserves_mton', strong_path('Coal', 'proven'))

        loader.add_xpath('petroleum_production_bbl_per_day', strong_path('Petroleum', 'total'))
        loader.add_xpath('petroleum_consumption_bbl_per_day', strong_path('Petroleum', 'refined'))
        loader.add_xpath('petroleum_exports_bbl_per_day', strong_path('Petroleum', 'exports'))
        loader.add_xpath('petroleum_imports_bbl_per_day', strong_path('Petroleum', 'imports'))
        loader.add_xpath('petroleum_estimated_reserves_bbl', strong_path('Petroleum', 'reserves'))

        loader.add_xpath('refined_petroleum_production_bbl_per_day', header_path('Refined petroleum products - production'))

        loader.add_xpath('refined_petroleum_exports_bbl_per_day', header_path('Refined petroleum products - exports'))

        loader.add_xpath('refined_petroleum_imports_bbl_per_day', header_path('Refined petroleum products - imports'))

        loader.add_xpath('natural_gas_production_meter3', strong_path('Natural gas', 'production'))
        loader.add_xpath('natural_gas_cunsuption_meter3', strong_path('Natural gas', 'consumption'))
        loader.add_xpath('natural_gas_exports_meter3', strong_path('Natural gas', 'exports'))
        loader.add_xpath('natural_gas_imports_meter3', strong_path('Natural gas', 'imports'))
        loader.add_xpath('natural_gas_proven_reserves_meter3', strong_path('Natural gas', 'proven'))

        loader.add_xpath('co2_emissions_total_mtons', header_path('Carbon dioxide emissions'))
        loader.add_xpath('co2_emissions_coal_and_coke_mtons', strong_path('Carbon dioxide emissions', 'coal'))
        loader.add_xpath('co2_emissions_petroleum_mtons', strong_path('Carbon dioxide emissions', 'petroleum'))
        loader.add_xpath('co2_emissions_natural_gas_mtons', strong_path('Carbon dioxide emissions', 'natural'))

        loader.add_xpath('energy_consumption_per_capita_btu', header_path('Energy consumption per capita'))

        loader.add_xpath('telephone_landline_subscriptions_total', strong_path('Telephones - fixed lines', 'total'))
        loader.add_xpath('telephone_landline_subscriptions_per_100', strong_path('Telephones - fixed lines', '100'))

        loader.add_xpath('mobile_phone_subscriptions_total', strong_path('Telephones - mobile cellular', 'total'))
        loader.add_xpath('mobile_phone_subscriptions_per_100', strong_path('Telephones - mobile cellular', '100'))

        loader.add_xpath('internet_users_total', strong_path('Internet users', 'total'))
        loader.add_xpath('internet_users_per_pop', strong_path('Internet users', 'percent'))

        loader.add_xpath('fixed_broadband_subscriptions_total', strong_path('Broadband - fixed subscriptions', 'total'))
        loader.add_xpath('fixed_broadband_subscriptions_per_100', strong_path('Broadband - fixed subscriptions', '100'))

        loader.add_xpath('registered_airlines_quantity', strong_path('National air transport system', 'number'))
        loader.add_xpath('registered_airlines_number_of_aircraft', strong_path('National air transport system', 'inventory'))
        loader.add_xpath('annual_airline_passenger_traffic', strong_path('National air transport system', 'passenger'))
        loader.add_xpath('annual_airline_freight_traffic', strong_path('National air transport system', 'freight'))

        loader.add_xpath('civil_aircraft_registration_code_prefix', header_path('civil_aircraft_registration_code_prefix'))

        loader.add_xpath('airports_total', strong_path('Airports', 'total'))

        loader.add_xpath('airports_paved_total', strong_path('Airports - with paved runways', 'total'))
        loader.add_xpath('airports_paved_over_3047m', strong_path('Airports - with paved runways', 'over'))
        loader.add_xpath('airports_paved_2438_to_3047m', strong_path('Airports - with paved runways', '2,438'))
        loader.add_xpath('airports_paved_1524_to_2437m', strong_path('Airports - with paved runways', '1,524'))
        loader.add_xpath('airports_paved_914_to_1523m', strong_path('Airports - with paved runways', '914'))
        loader.add_xpath('airports_paved_under_914m', strong_path('Airports - with paved runways', 'under'))

        loader.add_xpath('airports_unpaved_total', strong_path('Airports - with unpaved runways', 'total'))
        loader.add_xpath('airports_unpaved_over_3047m', strong_path('Airports - with unpaved runways', 'over'))
        loader.add_xpath('airports_unpaved_2438_to_3047m', strong_path('Airports - with unpaved runways', '2,438'))
        loader.add_xpath('airports_unpaved_1524_to_2437m', strong_path('Airports - with unpaved runways', '1,524'))
        loader.add_xpath('airports_unpaved_914_to_1523m', strong_path('Airports - with unpaved runways', '914'))
        loader.add_xpath('airports_unpaved_under_914m', strong_path('Airports - with unpaved runways', 'under'))

        loader.add_xpath('heliports_total', header_path('Heliports'))

        loader.add_xpath('railways_total', strong_path('Railways', 'total'))
        loader.add_xpath('railways_standard_gauge', strong_path('Railways', 'standard'))
        loader.add_xpath('railways_narrow_gauge', strong_path('Railways', 'narrow'))
        loader.add_xpath('railways_broad_gauge', strong_path('Railways', 'broad'))
        loader.add_xpath('railways_dual_gauge', strong_path('Railways', 'dual'))

        loader.add_xpath('roads_total_km', strong_path('Roadways', 'total'))
        loader.add_xpath('roads_paved_km', strong_path('Roadways', 'paved'))
        loader.add_xpath('roads_unpaved_km', strong_path('Roadways', 'unpaved'))
        loader.add_xpath('roads_urban_km', strong_path('Roadways', 'urban'))
        loader.add_xpath('roads_non_urban_km', strong_path('Roadways', 'non-urban'))

        loader.add_xpath('waterways_km', header_path('Waterways'))

        loader.add_xpath('merchant_marine_watercraft_total', header_path('Merchant marine'))

        loader.add_xpath('military_expenditures_per_gdp', header_path('Military expenditures'))

        yield loader.load_item()


'''
scrapy crawl wfb_data -O country_data.json
'''
