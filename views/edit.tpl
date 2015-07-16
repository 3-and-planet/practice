% rebase('base.tpl')

<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">

    % #ヘッダ名の設定
    % if request.path == "/books/add":
        <h1 class="page-header">登録</h1>
    % else:
        <h1 class="page-header">編集</h1>
    % end

    <div class="col-md-5">

    % #<form>のアクション要素の設定

    % if request.path == "/books/add":
        <form action="/books/add" method="post">
    % else:
        <form action="/books/{{book.id}}/edit" method="post">
    % end

    <div class="form-group">

        % # タイトル要素の描画
        {{ !form.title.label }}
        {{ !form.title(class_="form-control", placeholder="タイトルを入力", maxlength="100") }}

        % # エラー内容の表示
        % if form.title.errors:
            <div class="errors">
            % for error in form.title.errors:
                <p class="text-danger">{{ error }}</p>
            % end
            </div>
        % end

    </div>

    <div class="form-group">

        % #価格要素の描画
        {{ !form.price.label }}
        {{ !form.price(class_="form-control", placeholder="価格を入力", maxlength="100") }}

        % #エラー内容の表示
        % if form.price.errors:
            <div class="errors">
            % for error in form.price.errors:
                <p class="text-danger">{{ error }}</p>
            % end
            </div>
        % end

    </div>

    <div class="form-group">

        % #メモ要素の描画
        {{ !form.memo.label }}
        {{ !form.memo(class_="form-control", placeholder="memoを入力", maxlength="100") }}

        % #エラー内容の表示
        % if form.memo.errors:
            <div class="errors">
            % for error in form.memo.errors:
                <p class="text-danger">{{ error }}</p>
            % end
            </div>
        % end

    </div>

        % # submitボタン表示設定
        % if request.path == "/books/add":
            <input type="submit" class="btn btn-default" value="作成する"/>
        % else:
            <input type="submit" class="btn btn-default" value="更新する"/>
        % end

        </form>
    </div>
</div>




