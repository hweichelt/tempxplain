<script>
    import "./app.css";
</script>

<body class="bg-background">
    <div id="content">
        <header class="border-b p-4">
            <div>TempXplain</div>
        </header>
        <main>
            <div id="graph" class="p-4">GRAPH</div>
            <div id="visualization" class="border-l grid grid-rows-2">
                <div class="p-4">REF</div>
                <div class="border-t p-4">FOIL</div>
            </div>
            <div id="timeline" class="p-4 border-t">TIME</div>
        </main>
    </div>
</body>

<style>
    #content {
        display: grid;
        grid-template-rows: auto 1fr;
        width: 100vw;
        height: 100vh;
    }
    main {
        display: grid;
        grid-template-columns: 2fr 1fr;
        grid-template-rows: 2fr 1fr;
        grid-template-areas:
            "exp viz"
            "tim viz";
    }
    #graph {
        grid-area: exp;
    }
    #visualization {
        grid-row: viz;
    }
    #timeline {
        grid-area: tim;
    }
</style>
