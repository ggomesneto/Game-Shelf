def serialize(data):
        return {
           
            'title' : data['name'],
            'platforms' : data['platforms'],
            'description' : data['description'],
            'genres' : data['genres'],
            'developers' : data['developers'],
            'esrb_rating' : data['esrb_rating'],
            'metacritic' : data['metacritic'],
            'publishers' : data['publishers'],
            'released' : data['released'],
            'website' : data['website'],
            'stores' : data['stores'],
            'images' : [ data['background_image'], data['background_image_additional']]

        }




        