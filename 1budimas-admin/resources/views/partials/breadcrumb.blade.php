<!-- ============================================================== -->
<!-- Breadcrumb -->
<!-- ============================================================== -->
<div class="page-breadcrumb">
    <div class="row">
        <div class="col-12 d-flex no-block align-items-center mx-4 mt-2">
            <h4 class="page-titles font-20">Admin</h4>
        </div>
        <div class="col-12 d-flex no-block align-items-center mx-4">
            <h5 class="page-titles text-primary fw-normal">
                @unless(empty($content->breadcrumb))
                    @foreach($content->breadcrumb as $i)
                        {{ $i }}
                        @unless($loop->last)
                            <i class="mdi mdi-step-forward"></i>
                        @endunless
                    @endforeach
                @endunless
            </h5>
        </div>
    </div>
</div>
<!-- ============================================================== -->
<!-- End Breadcrumb -->
<!-- ============================================================== -->