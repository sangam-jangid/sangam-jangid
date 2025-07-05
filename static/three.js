import * as THREE from 'https://unpkg.com/three@0.165.0/build/three.module.js'
import { OrbitControls } from './OrbitControls.js'

const scene = new THREE.Scene()

const sphereGeometry = new THREE.SphereGeometry(1, 32, 32)

const sphereMaterial = new THREE.MeshBasicMaterial({color: 'red'})

const sphere = new THREE.Mesh(
    sphereGeometry,
    sphereMaterial
)

sphere.scale.setScalar(5)

let url = 'https://my.spline.design/untitled-EcfsOG6JCDmvf96lk5SwV9pG/'

scene.add(url)

const axesHelper = new THREE.AxesHelper(2)
sphere.add(axesHelper)

const camera = new THREE.PerspectiveCamera(
35,
window.innerWidth / window.innerHeight,
0.1,
200
)

camera.position.z = 100

scene.add(camera)

const canvas = document.querySelector(".threejs")
const renderer = new THREE.WebGLRenderer({
  canvas:canvas,
  antialias: true
})

renderer.setSize(window.innerWidth, window.innerHeight)

const controls = new OrbitControls(camera, canvas)

window.addEventListener('resize', () =>{
    console.log("resized!")
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()
    renderer.setSize(window.innerWidth, window.innerHeight)
  
  })

const renderloop = () =>{
    controls.update()
    renderer.render(scene, camera)
    window.requestAnimationFrame(renderloop)
  }

renderloop()