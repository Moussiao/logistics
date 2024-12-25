import type { AxiosResponse } from 'axios';

import responseCaseMiddleware from './responseCaseMiddleware';

const onResponseFulfilled = async (response: AxiosResponse, enableCaseMiddleware: boolean) => {
  if (response.data) {
    response.data = responseCaseMiddleware(response.data, enableCaseMiddleware);
  }

  return response;
};

export default onResponseFulfilled;
