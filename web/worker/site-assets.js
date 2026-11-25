const icon='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 192"><rect width="192" height="192" rx="32" fill="#173d2e"/><text x="96" y="135" text-anchor="middle" font-family="Georgia,serif" font-size="132" font-weight="bold" fill="#f4f7f3">E</text></svg>';
export const siteAssets={
 '/icon.svg':{type:'image/svg+xml',body:icon},
 '/manifest.webmanifest':{type:'application/manifest+json',body:JSON.stringify({name:'EPSTMC · Evidence and context',short_name:'EPSTMC',description:'Source-linked stories, context and conditional scenarios',start_url:'/#/',scope:'/',display:'standalone',background_color:'#f4f7f3',theme_color:'#173d2e',icons:[{src:'/icon.svg',sizes:'any',type:'image/svg+xml',purpose:'any'}]})}
};
