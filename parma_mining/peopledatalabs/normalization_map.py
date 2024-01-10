"""Pre-defined normalization map for the module."""


class PdlNormalizationMap:
    """Class for the PDL Normalization Map."""

    map_json = {
        "Source": "peopledatalabs",
        "Mappings": [
            {
                "SourceField": "name",
                "DataType": "text",
                "MeasurementName": "company name",
            },
            {
                "SourceField": "display_name",
                "DataType": "text",
                "MeasurementName": "company display name",
            },
            {
                "SourceField": "size",
                "DataType": "text",
                "MeasurementName": "company size",
            },
            {
                "SourceField": "employee_count",
                "DataType": "int",
                "MeasurementName": "company employee count",
            },
            {
                "SourceField": "id",
                "DataType": "text",
                "MeasurementName": "company pdl id",
            },
            {
                "SourceField": "founded",
                "DataType": "int",
                "MeasurementName": "company founded year",
            },
            {
                "SourceField": "industry",
                "DataType": "text",
                "MeasurementName": "company industry",
            },
            {
                "SourceField": "naics",
                "DataType": "nested",
                "MeasurementName": "company naics",
                "NestedMappings": [
                    {
                        "SourceField": "naics_code",
                        "DataType": "text",
                        "MeasurementName": "company naics code",
                    },
                    {
                        "SourceField": "sector",
                        "DataType": "text",
                        "MeasurementName": "company naics sector",
                    },
                    {
                        "SourceField": "sub_sector",
                        "DataType": "text",
                        "MeasurementName": "company naics sub sector",
                    },
                    {
                        "SourceField": "industry_group",
                        "DataType": "text",
                        "MeasurementName": "company naics industry group",
                    },
                    {
                        "SourceField": "naics_industry",
                        "DataType": "text",
                        "MeasurementName": "company naics industry",
                    },
                    {
                        "SourceField": "national_industry",
                        "DataType": "text",
                        "MeasurementName": "company naics national industry",
                    },
                ],
            },
            {
                "SourceField": "sic",
                "DataType": "nested",
                "MeasurementName": "company sic",
                "NestedMappings": [
                    {
                        "SourceField": "sic_code",
                        "DataType": "text",
                        "MeasurementName": "company sic code",
                    },
                    {
                        "SourceField": "major_group",
                        "DataType": "text",
                        "MeasurementName": "company sic major group",
                    },
                    {
                        "SourceField": "industry_group",
                        "DataType": "text",
                        "MeasurementName": "company sic industry group",
                    },
                    {
                        "SourceField": "industry_sector",
                        "DataType": "text",
                        "MeasurementName": "company sic industry sector",
                    },
                ],
            },
            {
                "SourceField": "location",
                "DataType": "nested",
                "MeasurementName": "company location",
                "NestedMappings": [
                    {
                        "SourceField": "name",
                        "DataType": "text",
                        "MeasurementName": "company location name",
                    },
                    {
                        "SourceField": "locality",
                        "DataType": "text",
                        "MeasurementName": "company location locality",
                    },
                    {
                        "SourceField": "region",
                        "DataType": "text",
                        "MeasurementName": "company location region",
                    },
                    {
                        "SourceField": "metro",
                        "DataType": "text",
                        "MeasurementName": "company location metro",
                    },
                    {
                        "SourceField": "country",
                        "DataType": "text",
                        "MeasurementName": "company location country",
                    },
                    {
                        "SourceField": "continent",
                        "DataType": "text",
                        "MeasurementName": "company location continent",
                    },
                    {
                        "SourceField": "street_address",
                        "DataType": "text",
                        "MeasurementName": "company location street address",
                    },
                    {
                        "SourceField": "address_line_2",
                        "DataType": "text",
                        "MeasurementName": "company location address line 2",
                    },
                    {
                        "SourceField": "postal_code",
                        "DataType": "text",
                        "MeasurementName": "company location postal_code",
                    },
                    {
                        "SourceField": "geo",
                        "DataType": "text",
                        "MeasurementName": "company location geo",
                    },
                ],
            },
            {
                "SourceField": "linkedin_id",
                "DataType": "text",
                "MeasurementName": "company linkedin id",
            },
            {
                "SourceField": "linkedin_url",
                "DataType": "link",
                "MeasurementName": "company linkedin url",
            },
            {
                "SourceField": "facebook_url",
                "DataType": "link",
                "MeasurementName": "company facebook url",
            },
            {
                "SourceField": "twitter_url",
                "DataType": "link",
                "MeasurementName": "company twitter url",
            },
            {
                "SourceField": "profiles",
                "DataType": "link",
                "MeasurementName": "company profiles",
            },
            {
                "SourceField": "website",
                "DataType": "link",
                "MeasurementName": "company website",
            },
            {
                "SourceField": "gics_sector",
                "DataType": "text",
                "MeasurementName": "company gics sector",
            },
            {
                "SourceField": "mic_exchange",
                "DataType": "text",
                "MeasurementName": "company mic exchange",
            },
            {
                "SourceField": "type",
                "DataType": "text",
                "MeasurementName": "company type",
            },
            {
                "SourceField": "summary",
                "DataType": "text",
                "MeasurementName": "company summary",
            },
            {
                "SourceField": "tags",
                "DataType": "text",
                "MeasurementName": "company tags",
            },
            {
                "SourceField": "headline",
                "DataType": "text",
                "MeasurementName": "company headline",
            },
            {
                "SourceField": "alternative_names",
                "DataType": "text",
                "MeasurementName": "company alternative names",
            },
            {
                "SourceField": "alternative_domains",
                "DataType": "link",
                "MeasurementName": "company alternative domains",
            },
            {
                "SourceField": "affiliated profiles",
                "DataType": "text",
                "MeasurementName": "company affiliated profiles",
            },
        ],
    }

    def get_normalization_map(self):
        """Getter for the normalization map."""
        return self.map_json
