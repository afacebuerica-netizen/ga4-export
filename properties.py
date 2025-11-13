"""
GA4 Property Configuration.
Define your GA4 properties here with their mapping to website names and hostnames.

To find your GA4 Property ID:
1. Go to Google Analytics 4
2. Navigate to Admin > Property Settings
3. Your Property ID is at the top (e.g., '123456789')

Format:
'properties/PROPERTY_ID': {
    'name': 'Human-readable website name',
    'hostname': 'https://www.example.com'
}
"""

GA4_PROPERTIES = {
    # Example property - replace with your actual properties
        'properties/292104262':{'name':'1st Choice Dating','hostname':'1stchoicedating.com'},
    'properties/301937111':{'name':'1st Latin Women','hostname':'1stlatinwomen.com'},
    'properties/301951642':{'name':'A New Bride','hostname':'ANewBride.Com'},
    'properties/301924109':{'name':'Anewwife','hostname':'ANewWife.Com'},
    'properties/299583942':{'name':'A-Foreign-Affair','hostname':'a-foreign-affair.com'},
    # 'properties/498237196':{'name':'AFA Bangkok','hostname':'afabangkok.com'},
    'properties/302941692':{'name':'Acapulco Women','hostname':'acapulcowomen.com'},
    'properties/308094759':{'name':'Asian Love Mates','hostname':'asianlovemates.com'},
    # 'properties/301770685':{'name':'Asian Women','hostname':'asian-women.com'}, 
    # 'properties/301953791':{'name':'Bangkok-Women','hostname':'bangkok-women.com'},
    # 'properties/308134492':{'name':'Barranquilla Dating','hostname':'BarranquillaDating.Com'},
#     'properties/327641688':{'name':'Barranquilla Singles','hostname':'barranquillasingles.com'},
#     'properties/327661689':{'name':'Barranquilla Women','hostname':'barranquillawomen.com'},
#     'properties/490297016':{'name':'Love Me','hostname':'loveme.com'},
#     'properties/301944804':{'name':'Cali Women','hostname':'cali-women.com'},
#     'properties/301947209':{'name':'Cartagena Dating','hostname':'cartagenadating.com'},
#     'properties/327619169':{'name':'Cartagena Women','hostname':'cartagenawomen.com'},
#     'properties/301925674':{'name':'Cebu Women','hostname':'cebuwomen.com'},
#     'properties/301934685':{'name':'China Brides','hostname':'china-brides.com'},
#     'properties/327639574':{'name':'City of Brides','hostname':'cityofbrides.com'},
#     #'properties/355967372':{'name':'ColombianDating.com','hostname':'ColombianDating.Com'},
#     'properties/327653311':{'name':'Colombian Lady','hostname':'colombianlady.com'},
#     'properties/327674016':{'name':'Colombian Woman','hostname':'colombianwoman.com'},
#     'properties/327638761':{'name':'Costa-Rica-Women','hostname':'costa-rica-women.com'},
#     'properties/465344682':{'name':'Date Fit Girls','hostname':'datefit.com'},
#     #'properties/327658663':{'name':'Date Sites','hostname':'datesites.com'},
#     'properties/285039147':{'name':'Davao Women','hostname':'davaowomen.com'},
#     'properties/465333810':{'name':'Euro Love Mates ','hostname':'eurolovemates.com'},
    # 'properties/301909261':{'name':'Filipino Bride','hostname':'filipino-bride.com'},
#     'properties/465254704':{'name':'Foreign Ladies','hostname':'foreignladies.com'},
#     'properties/327669167':{'name':'Foreign Love Mates','hostname':'foreignlovemates.com'},
#     'properties/327689267':{'name':'Foreign Affair','hostname':'foreign-affair.net'},
#     # 'properties/327626246':{'name':'International Dating Club','hostname':'internationaldatingclub.com'},
#     'properties/327686340':{'name':'International-Dating','hostname':'international-dating.com'},
#     'properties/327685230':{'name':'Island Ladies','hostname':'islandladies.com'},
#     # 'properties/490290756':{'name':'loveme.com','hostname':'loveme.com'},
#     'properties/301961157':{'name':'Kiev Personals','hostname':'KievPersonals.Com'},
#     'properties/304730003':{'name':'Kiev Women','hostname':'kievwomen.com'},
#     'properties/327651090':{'name':'Latin-Personals','hostname':'Latin-personals.com'},
#     # 'properties/465335765':{'name':'Latina Love Mates','hostname':'latinlovemates.com'}, #to remove
#     'properties/327642308':{'name':'Manila-Women','hostname':'manila-women.com'},
#     'properties/301929541':{'name':'Medellin Dating','hostname':'medellindating.com'},
#     'properties/327688263':{'name':'Medellin Singles - GA4','hostname':'medellinsingles.com'},
#     'properties/301936503':{'name':'Medellin Women','hostname':'MedellinWomen.Com'},
#     'properties/327638379':{'name':'Mexican Love Mates','hostname':'MexicanLoveMates.Com'},
#     # 'properties/313999569':{'name':'Mexico City Dating','hostname':'mexicocitydating.com'},
#     'properties/327639673':{'name':'Moscow Ladies','hostname':'moscowladies.com'},
#     'properties/327664028':{'name':'My Dream Asian','hostname':'mydreamasian.com'},
#     'properties/301128255':{'name':'My Mail Order Bride','hostname':'mymailorderbride.com'},
#     'properties/301094791':{'name':'OdessaWomen','hostname':'OdessaWomen.com'},
#     'properties/327628765':{'name':'Peru Women','hostname':'peru-women.com'},
#     # 'properties/358871042':{'name':'Perudating.com','hostname':'perudating.com'},
#     'properties/285060325':{'name':'Philippine Women','hostname':'philippine-women.com'},
#     'properties/301131889':{'name':'Poltava Women','hostname':'Poltavawomen.Com'},
#     'properties/285018866':{'name':'Russia Ladies','hostname':'russia-ladies.com'},
#     'properties/284911393':{'name':'Saint-Petersburg-Women','hostname':'saint-petersburg-women.com'},
#     'properties/450807073':{'name':'Shanghai Women GA4','hostname':'shanghai-women.com'}, #no access to this property
#     'properties/400827427':{'name':'Foreign Brides','hostname':'foreignbride.com'},#no access to this property
#     'properties/327673608':{'name':'Cebu Insights','hostname':'cebuinsights.com'},#no access to this property
#     'properties/308094758':{'name':'Angels of Passion','hostname':'angelsofpassion.com'},#no access to this property
#     'properties/301099138':{'name':'Shenzhen Women','hostname':'ShenzhenWomen.Com'},
#     'properties/465346076':{'name':'Single Women Online','hostname':'singlewomenonline.com'},
#     'properties/301100449':{'name':'Thailand Women','hostname':'Thailand-women.Com'},
#     'properties/327634734':{'name':'Ukraine Ladies','hostname':'UkraineLadies.Com'},
#     'properties/301146716':{'name':'Ukraine Singles','hostname':'UkraineSingles.Com'},
#     # 'properties/465352029':{'name':'World Love Mates','hostname':'worldlovemates.com'},
#     'properties/301770685':{'name':'asian-women','hostname':'asian-women.com'},
#     'properties/327673006':{'name':'colombian bride','hostname':'colombian-bride.com'},
#     'properties/355964462':{'name':'dateint.com','hostname':'dateint.com'},
#     'properties/301916278':{'name':'filipino-women','hostname':'filipino-women.com'},
#     #'properties/400807434':{'name':'international-dating.com','hostname':'international-dating.com'}, #to remove
#     'properties/327680785':{'name':'latinlovemates.com','hostname':'latinlovemates.com'},
#     'properties/301786153':{'name':'mexico-women','hostname':'mexico-women.com'},
#     'properties/327681596':{'name':'Russia Women Official','hostname':'russia-women.com'}
# #         'properties/987654321': {
#             'name': 'Another Website',
#             'hostname': 'https://www.another-website.com'
#         },
#         Add more properties as needed
#         'properties/ABC123456': {
#             'name': 'Third Website',
#             'hostname': 'https://www.third-website.com'
#         },
}

