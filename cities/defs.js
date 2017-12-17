"use strict";

// const tileSize = 1000;
const tileSize = 0.01;
const baseClientTileSize = 1024;

// the coordinate range limit
// minimum Longitude const firstTileX = 51.311407399704756;
// minimum Latitude const firstTileY = 22.528788200443138;
// maximum Longitude const lastTileX = 56.43632570051036; 
// maximum Latitude const lastTileY = 26.208355999955707;
const firstTileX = -123.00000000000000;
const firstTileY = 37.00000000000000;
const lastTileX = -122.00000000000000; 
const lastTileY = 38.000000000000000;

const tileCountX = (lastTileX - firstTileX) / tileSize + 1;
const tileCountY = (lastTileY - firstTileY) / tileSize + 1;

const maxRoadNodeCount = 343724;
const maxRoadLinkCount = 423541;
const maxRoadLinkPointCount = 1433365; // simplified from 2267772
const maxRoadLinkIndexCount = 2019648; // simplified from 3688462
const maxRoadCount = 85237;
const maxAddressCount = 343443;

// const quadtreeLeft = 51.311407399704756;
// const quadtreeTop = 22.528788200443138;
const quadtreeLeft = -123.00000000000000;
const quadtreeTop = 37.00000000000000;
const quadtreeSize = 13.1072;


module.exports = {
  tileSize: tileSize,
  baseClientTileSize: baseClientTileSize,

  firstTileX: firstTileX,
  firstTileY: firstTileY,
  lastTileX: lastTileX,
  lastTileY: lastTileY,

  tileCountX: tileCountX,
  tileCountY: tileCountY,

  totalWidth: tileCountX * tileSize,
  totalHeight: tileCountY * tileSize,
  totalBaseClientWidth: tileCountX * baseClientTileSize,
  totalBaseClientHeight: tileCountY * baseClientTileSize,

  maxGeometryItemCount: maxRoadNodeCount + maxRoadLinkCount + maxRoadCount + maxAddressCount,
  maxVertexCount: maxRoadNodeCount + maxRoadLinkPointCount,
  maxRoadNodeCount: maxRoadNodeCount,
  maxRoadLinkCount: maxRoadLinkCount,
  maxRoadLinkPointCount: maxRoadLinkPointCount,
  maxRoadLinkIndexCount: maxRoadLinkIndexCount,
  maxRoadCount: maxRoadCount,
  maxAddressCount: maxAddressCount,

  quadtreeLeft: quadtreeLeft,
  quadtreeTop: quadtreeTop,
  quadtreeSize: quadtreeSize,

  // Inner Circle
  // defaultCenterX: 528180.744,
  // defaultCenterY: 182584.548,

  // Default Center
  // defaultCenterX: 55.263481,
  // defaultCenterY: 25.193542,
  defaultCenterX: -122.431297,
  defaultCenterY: 37.773972,

  minZoom: 0,
  actualZoom: 2,
  defaultZoom: 7,
  maxZoom: 9,

  minLoaderPostingCount: 256,
  maxLoaderPostingCount: 1024,
  maxLoaderPostingDelay: 1000,

  textureSize: 1024,
  textureDataSize: 1024 * 1024
};

// NOTE: We assume textureDataSize >= maxRoadNodeCount + maxRoadLinkCount
