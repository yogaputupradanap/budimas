import { root } from "./root";
import { Loginn } from "./root/login";
import { dashboard } from "./root/dashboard";
import { DraftFakturPajakRoute } from "./root/draft-faktur-pajak";
import { DraftDetailFakturPajakRoute } from "./root/draft-faktur-pajak/detail-draft-faktur-pajak";
import { FinalFakturPajakRoute } from "./root/final-faktur-pajak";

export const routes = root.concat(
  dashboard,
  Loginn,
  DraftFakturPajakRoute,
  DraftDetailFakturPajakRoute,
  FinalFakturPajakRoute
);
