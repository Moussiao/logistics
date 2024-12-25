import {
  bindMiniAppCSSVars,
  bindThemeParamsCSSVars,
  bindViewportCSSVars,
  initMiniApp,
  initThemeParams,
  initViewport,
} from '@telegram-apps/sdk';

export const initTelegramMiniApp = async () => {
  const [miniApp] = initMiniApp();
  const [themeParams] = initThemeParams();
  const [viewportPromise] = initViewport();

  const viewport = await viewportPromise;

  // Generate Mini Apps related CSS-variables and track their changes.
  bindMiniAppCSSVars(miniApp, themeParams);
  bindThemeParamsCSSVars(themeParams);
  bindViewportCSSVars(viewport);
};
