import logo from './youku/index_76b1ab63e5ff.svg'
import heroOne from './youku/index_19364423647f.jpg'
import heroTwo from './youku/category_c48eefbc7507.jpg'
import heroThree from './youku/index_d05e81d13796.jpg'
import coverOne from './youku/index_0368058383d1.jpg'
import coverTwo from './youku/index_09bec5ed9835.jpg'
import coverThree from './youku/index_42efc554b195.jpg'
import coverFour from './youku/category_005418709c74.jpg'
import coverFive from './youku/category_35e34f360e96.jpg'
import coverSix from './youku/play_31046b68e34f.jpg'
import placeholder from './youku/placeholder.png'
import navMovie from './youku/index_703aac2720cd.png'
import navLive from './youku/index_5970311dac65.png'
import navSport from './youku/index_677e3bc3cda2.png'
import navPublic from './youku/index_2948d266a0ba.png'

const posterModules = import.meta.glob('./youku/*.{jpg,png,webp}', { eager: true, import: 'default' })
const posterNames = [
  'category_005418709c74.jpg',
  'index_0368058383d1.jpg',
  'index_09bec5ed9835.jpg',
  'index_42efc554b195.jpg',
  'category_05c89a773f5d.jpg',
  'category_0cefc91afc0b.jpg',
  'category_2b19d581d80c.jpg',
  'category_5424fc1f35f5.jpg',
  'category_5af431e13671.jpg',
  'category_690b217d5781.jpg',
  'category_6e7ae5e081e8.jpg',
  'category_74857b299e85.jpg',
  'category_7e52dc3025ee.jpg',
  'category_8e6c483a4fb1.jpg',
  'category_bdf2142031dd.jpg',
  'category_dfacda53d815.jpg',
  'category_e37d3d05e11c.jpg',
  'category_eebbf08fd4dd.jpg',
  'category_f48e3d7713eb.jpg',
  'index_1799d3e0ba03.jpg',
  'index_283e0b874d3c.jpg',
  'index_42f122b25601.jpg',
  'index_747dc34dfd9b.jpg',
  'index_7ce90eb44e8d.jpg',
  'index_8668d32b191d.jpg',
  'index_86d08a9c1da1.jpg',
  'index_a2d2bc267179.jpg',
  'index_a30f7f5f0e9a.jpg',
  'index_b05770369ba5.jpg',
  'index_bd143c9f38ad.jpg',
  'index_bd9a8665a47d.jpg',
  'index_c7c3b128480d.jpg',
  'index_ed844a3bb2a3.jpg',
  'index_f32f717a638d.jpg',
  'index_f75da59d2c4c.jpg',
  'index_fb1c8cbddfbd.jpg',
  'index_22acdf2e77e1.webp',
  'index_2dae4302f2b4.webp',
  'index_526eeee0442a.webp',
  'index_902dfe4821b9.webp',
  'style_859bc5dd0825.png'
]

export const posterPool = posterNames.map((name) => posterModules[`./youku/${name}`]).filter(Boolean)

export const assets = {
  logo,
  placeholder,
  navMovie,
  navLive,
  navSport,
  navPublic,
  hero: [heroOne, heroTwo, heroThree],
  covers: [coverOne, coverTwo, coverThree, coverFour, coverFive, coverSix],
  posters: posterPool
}
