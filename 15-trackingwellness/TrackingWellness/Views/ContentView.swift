//
//  ContentView.swift
//  TrackingWellness
//
//  Created by Zachary Sturman on 8/30/23.
//

import SwiftUI

struct ContentView: View {
    @State private var showingSheet = false
    @StateObject var sharedVM = SharedVM()
    
    var body: some View {
        NavigationStack {
            ListView(sharedVM: sharedVM)
                .toolbar {
                    ToolbarItem(placement: .navigationBarTrailing) {
                        Button(action: {
                            showingSheet.toggle()
                        }, label: {
                            Image(systemName: "plus")
                        })
                    }
                }
                .sheet(isPresented: $showingSheet) {
                    CreateEditView()
                }
            
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
