import React, { Component } from 'react'
import L from 'react-dom-factories'
L_ = React.createElement
import {LineChart, Line, XAxis, YAxis, CartesianGrid} from 'recharts'

transpose_01 = (obj)->
  k1 = Object.keys obj
  elem = obj[k1[0]]
  k2 = Object.keys elem
  len2 = k2.length
  result = {}

  # set up a dict
  for key in k2
    result = Object.assign result, [key]:{}

  for i in k1
    sanitylen = Object.keys(obj[i]).length
    if sanitylen!=len2
      console.error "Dimensions mismatch:",sanitylen,len2
      len2 = Math.min len2, sanitylen

    for j in [0..(len2-1)]
      result[j][i] = obj[i][j]
  result


#export default class Vis extends React.Component
export default Vis = (props)->
  {labelDim, domainLabel, data} = props
  if not labelDim
    labelDim = 0

  keys = Object.keys data
  if typeof (data[keys[0]]) != 'object'
    data = y:data, x:[0..(keys.length-1)]
    domainLabel='x'

  keys = Object.keys data

  if labelDim==0
    data = transpose_01 data
  if labelDim==1
    elem = data[keys[0]]
    keys = Object.keys elem

  data_keys = keys.filter (k)-> k!=domainLabel

  #convert to array
  data = Object.keys(data).map (d)->data[d]

  L.div className:'presenter graph',
    L_ LineChart, data:data, width:300, height:150,
      L_ XAxis, dataKey:domainLabel
      L_ YAxis,0
      L_ CartesianGrid, strokeDasharray:'3 3'
      for k in data_keys
        L_ Line,
          key:k
          stroke:'#c43a31'
          type:"monotone"
          dataKey:k

