from app import app 
from models import db , Product , Role




r1 = Role(
    role_name = "seller"
)

r2 = Role(
    role_name = "buyer"
)

f1 = Product(
    name = "Daffodil",
    color = "yellow",
    image = "https://www.almanac.com/sites/default/files/styles/opengraph/public/image_nodes/daffodil.jpg?itok=kELb7ZSC"
)

f2 = Product(
    name = "Daisy",
    color = "White",
    image = "https://images.immediate.co.uk/production/volatile/sites/10/2018/02/991b4fbc-37f5-43b2-9838-8e5c8f856bed-f628cc4.jpg?quality=90&resize=960%2C640"
)

f3 = Product(
    name = "Iris",
    color = "purple",
    image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR06NgAPW1tHRzdC5lW5xU0VKe41c1SBBferBRlMd5MfAbSme6roZdhd7VrQQvhA1PSSaU&usqp=CAU"
)

f4= Product(
    name = "Dahlia",
    color = "white",
    image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSTdR6wuMgiKkIktoKuCvTp2DyeDH9aYC9EvpdJQBPmHON9BwC4YgNZMMdD2kvIc_vcOwE&usqp=CAU"
)

f5= Product(
    name = "Begonia",
    color = "peach",
    image = "https://www.gardenia.net/storage/app/public/uploads/images/detail/PL110460Optimized.jpg"
)

f6= Product(
    name = "Lavender",
    color = "lavender",
    image = "https://www.gardendesign.com/pictures/images/900x705Max/site_3/english-lavender-lavandula-angustifolia-garden-design_11716.jpg"
)

f7= Product(
    name = "Lily",
    color = "pink",
    image = "https://www.almanac.com/sites/default/files/image_nodes/oriental-lily.jpg"
)

f8= Product(
    name = "Buttercup",
    color = "yellow",
    image = "https://i.guim.co.uk/img/media/69329e5bf7f47b54f69a16e83eaa4f3699ca775c/0_261_5155_3093/master/5155.jpg?width=1200&quality=85&auto=format&fit=max&s=b2f3f7c4421464f5c63decc97dac0ef5"
)

f9= Product(
    name = "Marigold",
    color = "orangered",
    image = "https://www.gardendesign.com/pictures/images/900x705Max/dream-team-s-portland-garden_6/marigold-flowers-orange-pixabay_12708.jpg"
)

f10= Product(
    name = "Rose",
    color = "red",
    image = "https://cdn.pixabay.com/photo/2019/09/23/05/55/red-rose-4497601_1280.jpg"
)

f11= Product(
    name = "Rudbeckia",
    color = "yellow",
    image = "https://www.flower-db.com/uploads/large_1ad59ad4-9f57-410e-9a58-10a1078ebb08.jpg"
)

f12= Product(
    name = "Sunflower",
    color = "yellow",
    image = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Sunflower_sky_backdrop.jpg/1200px-Sunflower_sky_backdrop.jpg"
)

f13= Product(
    name = "Tulip",
    color = "red",
    image = "https://5.imimg.com/data5/ZR/OO/EA/SELLER-34246236/tulip-flower-500x500.jpg"
)

f14= Product(
    name = "Laceleaf",
    color = "red",
    image = "https://www.plantopedia.com/wp-content/uploads/2017/03/anthurium-andreanum-n17.jpg"
)

f15= Product(
    name = "Cactus",
    color = "green",
    image = "https://debraleebaldwin.com/wp-content/uploads/Saguaro-cactus.jpg"
)


db.session.add_all([r1,r2,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15])
db.session.commit()