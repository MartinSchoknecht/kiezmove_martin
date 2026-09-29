
#fetching from offers DB
db_offers_input ={alpha:1, beta:2, gamma:3} #as an example 

def get_offers():
    return db_offers_input


#fetching from applicants DB
db_applicants_input = [{a:1,b:2}, {a:None,b:3}, {a:4,b:5}] #as an example

def get_applicants():
    return db_applicants_input

#defining transformation rules to be applied to the applicants data 
#rules will transform the applicants to match the relevant offers data wich will return 1 and missmatch 
# wich will return 0 for the soft skills and the difference between the applicants and offers for the hard skills
transformation_rules = {a: "1  if db_applicants_input[a] > db_offers_input[alpha] else 0", b: "db_applicants_input[b] - db_offers_input[beta]"}

def transform_applicants():
    transformed_applicants = []
    for applicant in db_applicants_input:
        transformed_applicant = {}
        for key, rule in transformation_rules.items():
            transformed_applicant[key] = eval(rule)
        transformed_applicants.append(transformed_applicant)
    return transformed_applicants

def calculate_overall_appeal_score(applicant):
    #will be done by Nadiia
    #will include missing data score and some distance to the offers
    return notImplemented

def part_offers_in_soft_and_hard_skills():
    offers = get_offers()
    soft_skills = {k: v for k, v in offers.items() if k in ['alpha', 'beta']} 
    hard_skills = {k: v for k, v in offers.items() if k in ['gamma']}
    return soft_skills, hard_skills

soft_skills, hard_skills = part_offers_in_soft_and_hard_skills()

def filter_not_matching_applicants():
    transformed_applicants = transform_applicants()
    #1st filter for applicants who do not match hard skills
    for hard_skill in hard_skills:
        transformed_applicants = [applicant for applicant in transformed_applicants if applicant[hard_skill] > 0 ]

    #2nd count for each applicants the matching soft skills
    for soft_skill in soft_skills:
        for applicant in transformed_applicants:
            if applicant[soft_skill] == 1:
                applicant['matching_soft_skills'] = applicant.get('matching_soft_skills', 0) + 1
            else:
                applicant['matching_soft_skills'] = applicant.get('matching_soft_skills', 0)

    #3rd order the applicants by the number of matching soft skills in descending order and return the top 5 applicants
    transformed_applicants.sort(key=lambda x: x['matching_soft_skills'], reverse=True)
    
    return transformed_applicants[:5]

