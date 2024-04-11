from django import forms
import pycountry


class SearchForm(forms.Form):
    month = forms.ChoiceField(
        label='Choose the month of your unforgettable trip',
        choices=[
            ('January', 'January'),
            ('February', 'February'),
            ('March', 'March'),
            ('April', 'April'),
            ('May', 'May'),
            ('June', 'June'),
            ('July', 'July'),
            ('August', 'August'),
            ('September', 'September'),
            ('October', 'October'),
            ('November', 'November'),
            ('December', 'December')
        ])
    # from db, manually
    country = forms.ChoiceField(
        label='What country would you like to travel to?',
        choices=[('Afghanistan', 'Afghanistan'), ('Albania', 'Albania'),
                 ('Algeria', 'Algeria'), ('American Samoa', 'American Samoa'),
                 ('Andorra', 'Andorra'), ('Angola', 'Angola'), ('Anguilla', 'Anguilla'),
                 ('Antigua & Barbuda', 'Antigua & Barbuda'), ('Argentina', 'Argentina'),
                 ('Armenia', 'Armenia'), ('Aruba', 'Aruba'), ('Australia', 'Australia'),
                 ('Austria', 'Austria'), ('Azerbaijan', 'Azerbaijan'), ('Bahamas', 'Bahamas'),
                 ('Bahrain', 'Bahrain'), ('Bangladesh', 'Bangladesh'),
                 ('Barbados', 'Barbados'), ('Belarus', 'Belarus'), ('Belgium', 'Belgium'),
                 ('Belize', 'Belize'), ('Benin', 'Benin'), ('Bermuda', 'Bermuda'),
                 ('Bhutan', 'Bhutan'), ('Bolivia', 'Bolivia'),
                 ('Bonaire, Sint Eustatius and Saba', 'Bonaire, Sint Eustatius and Saba'),
                 ('Bosnia Herzegovina', 'Bosnia Herzegovina'), ('Botswana', 'Botswana'),
                 ('Brazil', 'Brazil'), ('British Virgin Islands', 'British Virgin Islands'),
                 ('Brunei Darussalam', 'Brunei Darussalam'), ('Bulgaria', 'Bulgaria'),
                 ('Burkina Faso', 'Burkina Faso'), ('Burundi', 'Burundi'),
                 ('Cambodia', 'Cambodia'), ('Cameroon', 'Cameroon'), ('Canada', 'Canada'),
                 ('Cape Verde', 'Cape Verde'), ('Cayman Islands', 'Cayman Islands'),
                 ('Chad', 'Chad'), ('Chile', 'Chile'), ('China', 'China'),
                 ('Colombia', 'Colombia'), ('Comoros', 'Comoros'),
                 ('Cook Islands', 'Cook Islands'), ('Costa Rica', 'Costa Rica'),
                 ("Cote D'ivoire", "Cote D'ivoire"), ('Croatia', 'Croatia'),
                 ('Curacao', 'Curacao'), ('Cyprus', 'Cyprus'),
                 ('Czech Republic', 'Czech Republic'),
                 ('Democratic Republic of the Congo', 'Democratic Republic of the Congo'),
                 ('Denmark', 'Denmark'), ('Djibouti', 'Djibouti'),
                 ('Dominica', 'Dominica'), ('Dominican Republic', 'Dominican Republic'),
                 ('Ecuador', 'Ecuador'), ('Egypt', 'Egypt'), ('El Salvador', 'El Salvador'),
                 ('Equatorial Guinea', 'Equatorial Guinea'), ('Eritrea', 'Eritrea'),
                 ('Estonia', 'Estonia'), ('Eswatini', 'Eswatini'), ('Ethiopia', 'Ethiopia'),
                 ('Faroe Islands', 'Faroe Islands'),
                 ('Federated States of Micronesia', 'Federated States of Micronesia'),
                 ('Fiji', 'Fiji'), ('Finland', 'Finland'), ('France', 'France'),
                 ('French Guiana', 'French Guiana'), ('French Polynesia', 'French Polynesia'),
                 ('Gabon', 'Gabon'), ('Gambia', 'Gambia'), ('Georgia', 'Georgia'),
                 ('Germany', 'Germany'), ('Ghana', 'Ghana'), ('Gibraltar', 'Gibraltar'),
                 ('Greece', 'Greece'), ('Greenland', 'Greenland'), ('Grenada', 'Grenada'),
                 ('Guadeloupe', 'Guadeloupe'), ('Guam', 'Guam'), ('Guatemala', 'Guatemala'),
                 ('Guernsey', 'Guernsey'), ('Guinea', 'Guinea'),
                 ('Guinea-Bissau', 'Guinea-Bissau'), ('Guyana', 'Guyana'), ('Haiti', 'Haiti'),
                 ('Honduras', 'Honduras'), ('Hong Kong SAR, China', 'Hong Kong SAR, China'),
                 ('Hungary', 'Hungary'), ('Iceland', 'Iceland'), ('India', 'India'),
                 ('Indonesia', 'Indonesia'), ('Iraq', 'Iraq'), ('Ireland', 'Ireland'),
                 ('Isle Of Man', 'Isle Of Man'), ('Israel', 'Israel'), ('Italy', 'Italy'),
                 ('Jamaica', 'Jamaica'), ('Japan', 'Japan'), ('Jersey', 'Jersey'),
                 ('Jordan', 'Jordan'), ('Kazakhstan', 'Kazakhstan'), ('Kenya', 'Kenya'),
                 ('Kosovo', 'Kosovo'), ('Kuwait', 'Kuwait'), ('Kyrgyzstan', 'Kyrgyzstan'),
                 ('Laos', 'Laos'), ('Latvia', 'Latvia'), ('Lebanon', 'Lebanon'),
                 ('Lesotho', 'Lesotho'), ('Liechtenstein', 'Liechtenstein'),
                 ('Lithuania', 'Lithuania'), ('Luxembourg', 'Luxembourg'),
                 ('Macau SAR, China', 'Macau SAR, China'), ('Madagascar', 'Madagascar'),
                 ('Malawi', 'Malawi'), ('Malaysia', 'Malaysia'), ('Maldives', 'Maldives'),
                 ('Mali', 'Mali'), ('Malta', 'Malta'), ('Martinique', 'Martinique'),
                 ('Mauritania', 'Mauritania'), ('Mauritius', 'Mauritius'),
                 ('Mayotte', 'Mayotte'), ('Mexico', 'Mexico'), ('Moldova', 'Moldova'),
                 ('Monaco', 'Monaco'), ('Mongolia', 'Mongolia'), ('Montenegro', 'Montenegro'),
                 ('Montserrat', 'Montserrat'), ('Morocco', 'Morocco'),
                 ('Mozambique', 'Mozambique'), ('Myanmar', 'Myanmar'), ('Namibia', 'Namibia'),
                 ('Nepal', 'Nepal'), ('Netherlands', 'Netherlands'),
                 ('New Caledonia', 'New Caledonia'), ('New Zealand', 'New Zealand'),
                 ('Nicaragua', 'Nicaragua'), ('Niger', 'Niger'), ('Nigeria', 'Nigeria'),
                 ('Niue', 'Niue'), ('Norfolk Island', 'Norfolk Island'),
                 ('North Macedonia', 'North Macedonia'),
                 ('Northern Mariana Islands', 'Northern Mariana Islands'), ('Norway', 'Norway'),
                 ('Oman', 'Oman'), ('Pakistan', 'Pakistan'), ('Palau', 'Palau'),
                 ('Palestinian Territory', 'Palestinian Territory'), ('Panama', 'Panama'),
                 ('Papua New Guinea', 'Papua New Guinea'), ('Paraguay', 'Paraguay'),
                 ('Peru', 'Peru'), ('Philippines', 'Philippines'), ('Poland', 'Poland'),
                 ('Portugal', 'Portugal'), ('Puerto Rico', 'Puerto Rico'), ('Qatar', 'Qatar'),
                 ('Republic of Congo', 'Republic of Congo'),
                 ('Reunion Island', 'Reunion Island'), ('Romania', 'Romania'),
                 ('Russia', 'Russia'), ('Rwanda', 'Rwanda'),
                 ('Saint Barthelemy', 'Saint Barthelemy'),
                 ('Saint Kitts And Nevis', 'Saint Kitts And Nevis'),
                 ('Saint Lucia', 'Saint Lucia'),
                 ('Saint Martin (France)', 'Saint Martin (France)'), ('Samoa', 'Samoa'),
                 ('San Marino', 'San Marino'),
                 ('Sao Tome and Principe', 'Sao Tome and Principe'),
                 ('Saudi Arabia', 'Saudi Arabia'), ('Senegal', 'Senegal'), ('Serbia', 'Serbia'),
                 ('Seychelles', 'Seychelles'), ('Sierra Leone', 'Sierra Leone'),
                 ('Singapore', 'Singapore'),
                 ('Sint Maarten (Netherlands)', 'Sint Maarten (Netherlands)'),
                 ('Slovakia', 'Slovakia'), ('Slovenia', 'Slovenia'),
                 ('Solomon Islands', 'Solomon Islands'), ('South Africa', 'South Africa'),
                 ('South Korea', 'South Korea'), ('South Sudan', 'South Sudan'),
                 ('Spain', 'Spain'), ('Sri Lanka', 'Sri Lanka'),
                 ('St. Vincent & Grenadines', 'St. Vincent & Grenadines'),
                 ('Suriname', 'Suriname'), ('Sweden', 'Sweden'), ('Switzerland', 'Switzerland'),
                 ('Taiwan', 'Taiwan'), ('Tajikistan', 'Tajikistan'), ('Tanzania', 'Tanzania'),
                 ('Thailand', 'Thailand'), ('Timor-Leste', 'Timor-Leste'), ('Togo', 'Togo'),
                 ('Tonga', 'Tonga'), ('Trinidad & Tobago', 'Trinidad & Tobago'),
                 ('Tunisia', 'Tunisia'), ('Turkey', 'Turkey'),
                 ('Turks & Caicos Islands', 'Turks & Caicos Islands'),
                 ('U.S. Virgin Islands', 'U.S. Virgin Islands'), ('Uganda', 'Uganda'),
                 ('Ukraine', 'Ukraine'), ('United Arab Emirates', 'United Arab Emirates'),
                 ('United Kingdom', 'United Kingdom'), ('United States', 'United States'),
                 ('Uruguay', 'Uruguay'), ('Uzbekistan', 'Uzbekistan'), ('Vanuatu', 'Vanuatu'),
                 ('Venezuela', 'Venezuela'), ('Vietnam', 'Vietnam'), ('Zambia', 'Zambia'),
                 ('Zimbabwe', 'Zimbabwe')])
